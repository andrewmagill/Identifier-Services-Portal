from agavepy.agave import Agave, AgaveException
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import (HttpResponse,
                         HttpResponseRedirect,
                         HttpResponseBadRequest,
                         HttpResponseForbidden,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from django.shortcuts import render
import json, logging
from ..forms.processes import ProcessTypeForm, ProcessFieldsForm
from ..models import Project, Specimen, Process
from ids.utils import (get_portal_api_client,
                       get_process_choices,
                       get_process_fields)
from helper import client, collapse_meta
from requests import HTTPError

logger = logging.getLogger(__name__)


@login_required
def list(request):
    """List all processes related to a specimen"""
    #######
    # GET #
    #######
    if request.method == 'GET':

        project_uuid = request.GET.get('project_uuid', None)
        specimen_uuid = request.GET.get('specimen_uuid', None)

        if not specimen_uuid and not project_uuid:
            messages.warning(request, 'Missing project or specimen UUID, cannot find processes.')
            return HttpResponseRedirect(reverse('ids_projects:project-list-private'))

        project = None
        specimen = None
        process = None

        try:
            if not specimen_uuid:
                project = Project(api_client=api_client, uuid=project_uuid)
                processes = project.processes
            else:
                specimen = Specimen(api_client=api_client, uuid=specimen_uuid)
                processes = specimen.processes
                project = Specimen.project

        except Exception as e:
            exception_msg = 'Unable to load project, specimen, or processes. %s' % e
            logger.error(exception_msg)
            messages.warning(request, exception_msg)
            return HttpResponseRedirect(reverse('ids_projects:project-list-private'))

        context = { 'project': project,
                    'specimen' : specimen,
                    'processes': processes
                  }

        return render(request, 'ids_projects/processes/index.html', context)

    #########
    # OTHER #
    #########
    else:
        return HttpResponseBadRequest("Method not allowed")


@login_required
def view(request, process_uuid):
    """ """
    #######
    # GET #
    #######
    if request.method == 'GET':

        if request.user.is_anonymous():
            api_client = get_portal_api_client()
        else:
            api_client = request.user.agave_oauth.api_client

        try:
            process = Process(api_client=api_client, uuid=process_uuid)
        except Exception as e:
            exception_msg = 'Unable to load process. %s' % e
            logger.error(exception_msg)
            messages.warning(request, exception_msg)
            return HttpResponseRedirect(reverse('ids_projects:project-list-private'))

        context = {'process' : process,
                   'project' : process.project,
                   'specimen' : process.specimen,
                   'datas' : process.data,
                   'inputs': process.inputs,
                   'outputs': process.outputs, }

        return render(request, 'ids_projects/processes/detail.html', context)

    #########
    # OTHER #
    #########
    else:
        return HttpResponseBadRequest("Method not allowed")


@login_required
def create(request):
    """Create a new process related to a specimen"""

    project_uuid = request.GET.get('project_uuid', None)
    specimen_uuid = request.GET.get('specimen_uuid', None)
    process_type = request.GET.get('process_type', None)

    if not specimen_uuid and not project_uuid:
        messages.warning(request, 'Missing project or specimen UUID, cannot find processes.')
        return HttpResponseRedirect(reverse('ids_projects:project-list-private'))

    api_client = request.user.agave_oauth.api_client

    project = None
    specimen = None

    try:
        if not specimen_uuid:
            project = Project(api_client=api_client, uuid=project_uuid)
        else:
            specimen = Specimen(api_client=api_client, uuid=specimen_uuid)
            project = specimen.project
    except Exception as e:
        exception_msg = 'Unable to load project or specimen, cannot create process. %s' % e
        logger.error(exception_msg)
        messages.warning(request, exception_msg)
        return HttpResponseRedirect(reverse('ids_projects:project-list-private'))

    try:
        process_type_choices = get_process_choices(project)
    except Exception as e:
        exception_msg = 'Missing project type information, cannot create process. %s' % e
        logger.error(exception_msg)
        messages.warning(request, exception_msg)
        return HttpResponseRedirect(
                    reverse('ids_projects:specimen-view',
                            kwargs={'specimen_uuid': specimen.uuid}))

    context = { 'project':project,
                'specimen':specimen }

    #######
    # GET #
    #######
    if request.method == 'GET' and process_type is None:
        context['form_process_type'] = form_process_type = ProcessTypeForm(process_type_choices)
        context['form_process_fields'] = None

    ########
    # POST #
    ########
    elif request.method == 'POST' or process_type is not None:

        process_type = request.GET.get('process_type', request.POST.get('process_type'))
        process_fields = get_process_fields(project, process_type)

        form_process_type = ProcessTypeForm(process_type_choices, initial={ 'process_type': process_type })
        form_process_type.fields['process_type'].widget.attrs['disabled'] = True
        form_process_type.fields['process_type'].widget.attrs['readonly'] = True

        #################################################
        # POST includes 'form_process_type' fields only #
        #################################################
        if not 'process_fields' in request.POST:
            form_process_fields = ProcessFieldsForm(process_fields)
            context['form_process_type'] = form_process_type
            context['form_process_fields'] = form_process_fields
            context['process_type'] = process_type

        ################################################################
        # POST includes form_process_type & form_process_fields fields #
        ################################################################
        else:
            form_process_fields = ProcessFieldsForm(process_fields, request.POST)

            if form_process_type.is_valid() and form_process_fields.is_valid():
                logger.debug('Process form is valid')

                data = {'process_type':process_type}
                data.update(form_process_type.cleaned_data.copy())
                data.update(form_process_fields.cleaned_data.copy())

                if project and not specimen:
                    associationIds = project.associationIds
                    associationIds.append(project.uuid)
                elif specimen:
                    associationIds = specimen.associationIds
                    associationIds.append(specimen.uuid)

                meta = { 'associationIds': associationIds, 'value': data }

                try:
                    process = Process(api_client=api_client, meta=meta)
                    process.save()

                    success_msg = 'Successfully created process.'
                    logger.info(success_msg)
                    messages.success(request, success_msg)
                    return HttpResponseRedirect(
                                reverse('ids_projects:process-view',
                                        kwargs={'process_uuid': process.uuid}))
                except HTTPError as e:
                    exception_msg = 'Unable to create new process. %s' % e
                    logger.error(exception_msg)
                    messages.error(request, exception_msg)
                    return HttpResponseRedirect(
                                reverse('ids_projects:specimen-view',
                                        kwargs={'specimen_uuid': specimen.uuid}))

    if request.is_ajax():
        return render(request, 'ids_projects/processes/get_fields_ajax.html', context)
    else:
        return render(request, 'ids_projects/processes/create.html', context)


@login_required
def edit(request, process_uuid):
    """Edit existing process metadata"""

    api_client = request.user.agave_oauth.api_client

    try:
        process = Process(api_client=api_client, uuid=process_uuid)
    except HTTPError as e:
        logger.error('Error editing process. {}'.format(e.message))
        messages.warning(request, 'Error editing process.')
        return HttpResponseRedirect('/process/{}'.format(process_uuid))
    except Exception as e:
        logger.error('Error editing process. {}'.format(e.message))
        messages.warning(request, 'Process not found.')
        return HttpResponseRedirect('/projects/private/')

    process_fields = get_process_fields(project)

    #######
    # GET #
    #######
    if request.method == 'GET':
        context = {'form_process_edit': ProcessFieldsForm(process_fields, initial=process.value),
                   'specimen': process.specimen,
                   'project': process.project,
                   'process': process}

        return render(request, 'ids_projects/processes/edit.html', context)

    ########
    # POST #
    ########
    elif request.method == 'POST':
        form = ProcessFieldsForm(process_fields, request.POST)

        if form.is_valid():

            try:
                process.value.update(form.cleaned_data)
                process.save()

                messages.info(request, 'Process successfully edited.')
                return HttpResponseRedirect(
                            reverse('ids_projects:process-view',
                                    kwargs={'process_uuid': process.uuid}))
            except Exception as e:
                exception_msg = 'Unable to edit process. %s' % e
                logger.error(exception_msg)
                messages.error(request, exception_msg)
                return HttpResponseRedirect(
                            reverse('ids_projects:process-view',
                                    kwargs={'process_uuid': process.uuid}))

@login_required
def delete(request, process_uuid):
    """Delete a process"""
    #######
    # GET #
    #######
    if request.method == 'GET':

        api_client = request.user.agave_oauth.api_client

        try:
            process = Process(api_client=api_client, uuid=specimen_uuid)
            specimen = process.specimen
            project = process.project
            process.delete()
        except Exception as e:
            exception_msg = 'Unable to delete process. %s' % e
            logger.exception(exception_msg)
            messages.warning(request, exception_msg)
            if specimen:
                return HttpResponseRedirect('/specimen/{}/'.format(specimen.uuid))
            else:
                return HttpResponseRedirect('/project/{}/'.format(project.uuid))

        messages.success(request, 'Successfully deleted process.')
        if specimen:
            return HttpResponseRedirect('/specimen/{}'.format(specimen.uuid))
        else:
            return HttpResponseRedirect('/project/{}'.format(project.uuid))

    #########
    # OTHER #
    #########
    else:
        return HttpResponseBadRequest("Method not allowed")
