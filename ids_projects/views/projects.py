from agavepy.agave import Agave, AgaveException
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import (HttpResponse,
                         HttpResponseRedirect,
                         HttpResponseBadRequest,
                         HttpResponseForbidden,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from django.shortcuts import render
from django.core.urlresolvers import reverse
from ids.utils import get_portal_api_client
from ..forms.projects import ProjectForm
from ..more_efficient_models import Project
from helper import client, collapse_meta
import json, logging

logger = logging.getLogger(__name__)


def list_public(request):
    """List public projects"""
    #######
    # GET #
    #######
    if request.method == 'GET':

        api_client = get_portal_api_client()

        try:
            project = Project(api_client=api_client)
            projects = project.list()
        except Exception as e:
            exception_msg = 'Unable to load projects. %s' % e
            logger.error(exception_msg)
            messages.warning(request, exception_msg)
            return HttpResponseRedirect('/')

        context = { 'type': 'public', 'public_projects':projects, 'create_button':True }

        return render(request, 'ids_projects/projects/index.html', context)

    #########
    # OTHER #
    #########
    else:
        return HttpResponseBadRequest("Method not allowed")


@login_required
def list_private(request):
    """List private projects"""
    #######
    # GET #
    #######
    if request.method == 'GET':

        api_client = request.user.agave_oauth.api_client

        try:
            project = Project(api_client=api_client)
            projects = project.list()
        except Exception as e:
            exception_msg = 'Unable to load projects. %s' % e
            logger.error(exception_msg)
            messages.warning(request, exception_msg)
            return HttpResponseRedirect('/')

        context = { 'type': 'private', 'private_projects': projects, 'create_button': True }

        return render(request, 'ids_projects/projects/index.html', context)

    #########
    # OTHER #
    #########
    else:
        return HttpResponseBadRequest("Method not allowed")


def view(request, project_uuid):
    """Queries project metadata and all associated metadata"""
    #######
    # GET #
    #######
    if request.method == 'GET':

        if request.user.is_anonymous():
            api_client = get_portal_api_client()
        else:
            api_client = request.user.agave_oauth.api_client

        try:
            project = Project(api_client=api_client, uuid=project_uuid)
        except Exception as e:
            exception_msg = 'Unable to load project. %s' % e
            logger.error(exception_msg)
            messages.warning(request, exception_msg)
            return HttpResponseRedirect('/projects/')

        context = {'project' : project,
                   'specimen_count' : len(project.specimens),
                   'process_count' : len(project.processes),
                   'file_count' : len(project.data)}

        return render(request, 'ids_projects/projects/detail.html', context)

    #########
    # OTHER #
    #########
    else:
        return HttpResponseBadRequest("Method not allowed")


@login_required
def create(request):
    """Create a new project"""
    api_client = request.user.agave_oauth.api_client

    #######
    # GET #
    #######
    if request.method == 'GET':

        context = {'form_project_create': ProjectForm(), 'project': None}
        return render(request, 'ids_projects/projects/create.html', context)

    ########
    # POST #
    ########
    elif request.method == 'POST':

        form = ProjectForm(request.POST)

        if form.is_valid():

            body = form.cleaned_data
            user_full = request.user.get_full_name()
            body.update({ 'creator': user_full })

            try:
                project = Project(api_client=api_client, body=body)
                result = project.save()

            except Exception as e:
                exception_msg = 'Unable to create new project. %s' % e
                logger.error(exception_msg)
                messages.warning(request, exception_msg)
                return HttpResponseRedirect('/projects/private/')

            if 'uuid' in result:
                messages.info(request, 'New project created.')
                return HttpResponseRedirect(
                            reverse('ids_projects:project-view',
                                    kwargs={'project_uuid': project.uuid}))

        warning_msg = 'Invalid API response. %s' % result
        logger.warning(warning_msg)
        messages.warning(request, warning_msg)
        return HttpResponseRedirect('/projects/private/')

    #########
    # OTHER #
    #########
    else:
        return HttpResponseBadRequest("Method not allowed")


@login_required
def edit(request, project_uuid):
    """Edit a project, given the uuid"""
    api_client = request.user.agave_oauth.api_client

    try:
        project = Project(api_client=api_client, uuid=project_uuid)
    except Exception as e:
        exception_msg = 'Unable to load project. %s' % e
        logger.exception(exception_msg)
        messages.warning(request, exception_msg)
        return HttpResponseRedirect('/projects/private/')

    #######
    # GET #
    #######
    if request.method == 'GET':

        context = { 'form_project_edit': ProjectForm(initial=project.body),
                    'project': project }
        return render(request, 'ids_projects/projects/create.html', context)

    ########
    # POST #
    ########
    elif request.method == 'POST':

        form = ProjectForm(request.POST)

        if form.is_valid():

            try:
                project.body = form.cleaned_data
                result = project.save()
            except Exception as e:
                exception_msg = 'Unable to create new project. %s' % e
                logger.error(exception_msg)
                messages.warning(request, exception_msg)
                return HttpResponseRedirect(
                            reverse('ids_projects:project-view',
                                    kwargs={ 'project_uuid': project.uuid }))

            if 'uuid' in result:
                messages.info(request, 'Project successfully edited.')
                return HttpResponseRedirect(
                            reverse('ids_projects:project-view',
                                    kwargs={ 'project_uuid': project.uuid }))

        warning_msg = 'Invalid API response. %s' % result
        logger.warning(warning_msg)
        messages.warning(request, warning_msg)
        return HttpResponseRedirect(
                    reverse('ids_projects:project-view',
                            kwargs={ 'project_uuid': project.uuid }))

    #########
    # OTHER #
    #########
    else:
        return HttpResponseBadRequest("Method not allowed")


@login_required
def make_public(request, project_uuid):
    """Make a project public"""
    #######
    # GET #
    #######
    if request.method == 'GET':

        # TODO: This needs to happen in the dataset

        # try:
        #     project = Project(uuid=project_uuid, user=request.user)
        #     project.make_public()
        # except Exception as e:
        #     exception_msg = 'Unable to make project and associated objects public.'
        #     logger.exception(exception_msg)
        #     messages.warning(request, exception_msg)
        #     return HttpResponseRedirect('/project/%s' % project_uuid)
        #
        # messages.success(request, 'Successfully made project public.')
        return HttpResponseRedirect('/project/%s' % project_uuid)

    #########
    # OTHER #
    #########
    else:
        return HttpResponseBadRequest("Method not allowed")


@login_required
def make_private(request, project_uuid):
    """Make a project private"""
    #######
    # GET #
    #######
    if request.method == 'GET':

        # TODO: This needs to happen in the dataset

        # try:
        #     project = Project(uuid=project_uuid, user=request.user)
        #     project.make_private()
        # except Exception as e:
        #     exception_msg = 'Unable to make project and associated objects public.'
        #     logger.exception(exception_msg)
        #     messages.warning(request, exception_msg)
        #     return HttpResponseRedirect('/project/%s' % project_uuid)
        #
        # messages.success(request, 'Successfully made project private.')
        return HttpResponseRedirect('/project/%s' % project_uuid)

    #########
    # OTHER #
    #########
    else:
        return HttpResponseBadRequest("Method not allowed")


@login_required
def delete(request, project_uuid):
    """Delete a project """
    api_client = request.user.agave_oauth.api_client

    #######
    # GET #
    #######
    if request.method == 'GET':

        api_client = request.user.agave_oauth.api_client

        try:
            project = Project(api_client=api_client, uuid=project_uuid)
            project.delete()
        except Exception as e:
            exception_msg = 'Unable to delete project. %s' % e
            logger.exception(exception_msg)
            messages.warning(request, exception_msg)
            return HttpResponseRedirect('/projects/private/')

        messages.success(request, 'Successfully deleted project.')
        return HttpResponseRedirect('/projects/private/')

    #########
    # OTHER #
    #########
    else:
        return HttpResponseBadRequest("Method not allowed")
