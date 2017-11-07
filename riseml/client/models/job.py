# coding: utf-8

"""
    RiseML API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 1.1.0
    Contact: contact@riseml.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from pprint import pformat
from six import iteritems
import re


class Job(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, id=None, short_id=None, slug=None, experiment_id=None, root=None, parent=None, previous_job=None, name=None, kind=None, role=None, state=None, desired_state=None, reason=None, message=None, exit_code=None, created_at=None, started_at=None, state_changed_at=None, finished_at=None, cpus=None, mem=None, gpus=None, image=None, node_selectors=None, service_name=None, external_service_name=None, service_ports=None, environment=None, commands=None, project=None, children=None):
        """
        Job - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'short_id': 'str',
            'slug': 'str',
            'experiment_id': 'str',
            'root': 'str',
            'parent': 'str',
            'previous_job': 'str',
            'name': 'str',
            'kind': 'str',
            'role': 'str',
            'state': 'str',
            'desired_state': 'str',
            'reason': 'str',
            'message': 'str',
            'exit_code': 'int',
            'created_at': 'int',
            'started_at': 'int',
            'state_changed_at': 'int',
            'finished_at': 'int',
            'cpus': 'float',
            'mem': 'int',
            'gpus': 'int',
            'image': 'str',
            'node_selectors': 'str',
            'service_name': 'str',
            'external_service_name': 'str',
            'service_ports': 'str',
            'environment': 'str',
            'commands': 'str',
            'project': 'Project',
            'children': 'list[Job]'
        }

        self.attribute_map = {
            'id': 'id',
            'short_id': 'short_id',
            'slug': 'slug',
            'experiment_id': 'experiment_id',
            'root': 'root',
            'parent': 'parent',
            'previous_job': 'previous_job',
            'name': 'name',
            'kind': 'kind',
            'role': 'role',
            'state': 'state',
            'desired_state': 'desired_state',
            'reason': 'reason',
            'message': 'message',
            'exit_code': 'exit_code',
            'created_at': 'created_at',
            'started_at': 'started_at',
            'state_changed_at': 'state_changed_at',
            'finished_at': 'finished_at',
            'cpus': 'cpus',
            'mem': 'mem',
            'gpus': 'gpus',
            'image': 'image',
            'node_selectors': 'node_selectors',
            'service_name': 'service_name',
            'external_service_name': 'external_service_name',
            'service_ports': 'service_ports',
            'environment': 'environment',
            'commands': 'commands',
            'project': 'project',
            'children': 'children'
        }

        self._id = id
        self._short_id = short_id
        self._slug = slug
        self._experiment_id = experiment_id
        self._root = root
        self._parent = parent
        self._previous_job = previous_job
        self._name = name
        self._kind = kind
        self._role = role
        self._state = state
        self._desired_state = desired_state
        self._reason = reason
        self._message = message
        self._exit_code = exit_code
        self._created_at = created_at
        self._started_at = started_at
        self._state_changed_at = state_changed_at
        self._finished_at = finished_at
        self._cpus = cpus
        self._mem = mem
        self._gpus = gpus
        self._image = image
        self._node_selectors = node_selectors
        self._service_name = service_name
        self._external_service_name = external_service_name
        self._service_ports = service_ports
        self._environment = environment
        self._commands = commands
        self._project = project
        self._children = children


    @property
    def id(self):
        """
        Gets the id of this Job.


        :return: The id of this Job.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Job.


        :param id: The id of this Job.
        :type: str
        """

        self._id = id

    @property
    def short_id(self):
        """
        Gets the short_id of this Job.


        :return: The short_id of this Job.
        :rtype: str
        """
        return self._short_id

    @short_id.setter
    def short_id(self, short_id):
        """
        Sets the short_id of this Job.


        :param short_id: The short_id of this Job.
        :type: str
        """

        self._short_id = short_id

    @property
    def slug(self):
        """
        Gets the slug of this Job.


        :return: The slug of this Job.
        :rtype: str
        """
        return self._slug

    @slug.setter
    def slug(self, slug):
        """
        Sets the slug of this Job.


        :param slug: The slug of this Job.
        :type: str
        """

        self._slug = slug

    @property
    def experiment_id(self):
        """
        Gets the experiment_id of this Job.


        :return: The experiment_id of this Job.
        :rtype: str
        """
        return self._experiment_id

    @experiment_id.setter
    def experiment_id(self, experiment_id):
        """
        Sets the experiment_id of this Job.


        :param experiment_id: The experiment_id of this Job.
        :type: str
        """

        self._experiment_id = experiment_id

    @property
    def root(self):
        """
        Gets the root of this Job.


        :return: The root of this Job.
        :rtype: str
        """
        return self._root

    @root.setter
    def root(self, root):
        """
        Sets the root of this Job.


        :param root: The root of this Job.
        :type: str
        """

        self._root = root

    @property
    def parent(self):
        """
        Gets the parent of this Job.


        :return: The parent of this Job.
        :rtype: str
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """
        Sets the parent of this Job.


        :param parent: The parent of this Job.
        :type: str
        """

        self._parent = parent

    @property
    def previous_job(self):
        """
        Gets the previous_job of this Job.


        :return: The previous_job of this Job.
        :rtype: str
        """
        return self._previous_job

    @previous_job.setter
    def previous_job(self, previous_job):
        """
        Sets the previous_job of this Job.


        :param previous_job: The previous_job of this Job.
        :type: str
        """

        self._previous_job = previous_job

    @property
    def name(self):
        """
        Gets the name of this Job.


        :return: The name of this Job.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Job.


        :param name: The name of this Job.
        :type: str
        """

        self._name = name

    @property
    def kind(self):
        """
        Gets the kind of this Job.


        :return: The kind of this Job.
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """
        Sets the kind of this Job.


        :param kind: The kind of this Job.
        :type: str
        """

        self._kind = kind

    @property
    def role(self):
        """
        Gets the role of this Job.


        :return: The role of this Job.
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """
        Sets the role of this Job.


        :param role: The role of this Job.
        :type: str
        """

        self._role = role

    @property
    def state(self):
        """
        Gets the state of this Job.


        :return: The state of this Job.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this Job.


        :param state: The state of this Job.
        :type: str
        """

        self._state = state

    @property
    def desired_state(self):
        """
        Gets the desired_state of this Job.


        :return: The desired_state of this Job.
        :rtype: str
        """
        return self._desired_state

    @desired_state.setter
    def desired_state(self, desired_state):
        """
        Sets the desired_state of this Job.


        :param desired_state: The desired_state of this Job.
        :type: str
        """

        self._desired_state = desired_state

    @property
    def reason(self):
        """
        Gets the reason of this Job.


        :return: The reason of this Job.
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """
        Sets the reason of this Job.


        :param reason: The reason of this Job.
        :type: str
        """

        self._reason = reason

    @property
    def message(self):
        """
        Gets the message of this Job.


        :return: The message of this Job.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this Job.


        :param message: The message of this Job.
        :type: str
        """

        self._message = message

    @property
    def exit_code(self):
        """
        Gets the exit_code of this Job.


        :return: The exit_code of this Job.
        :rtype: int
        """
        return self._exit_code

    @exit_code.setter
    def exit_code(self, exit_code):
        """
        Sets the exit_code of this Job.


        :param exit_code: The exit_code of this Job.
        :type: int
        """

        self._exit_code = exit_code

    @property
    def created_at(self):
        """
        Gets the created_at of this Job.


        :return: The created_at of this Job.
        :rtype: int
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this Job.


        :param created_at: The created_at of this Job.
        :type: int
        """

        self._created_at = created_at

    @property
    def started_at(self):
        """
        Gets the started_at of this Job.


        :return: The started_at of this Job.
        :rtype: int
        """
        return self._started_at

    @started_at.setter
    def started_at(self, started_at):
        """
        Sets the started_at of this Job.


        :param started_at: The started_at of this Job.
        :type: int
        """

        self._started_at = started_at

    @property
    def state_changed_at(self):
        """
        Gets the state_changed_at of this Job.


        :return: The state_changed_at of this Job.
        :rtype: int
        """
        return self._state_changed_at

    @state_changed_at.setter
    def state_changed_at(self, state_changed_at):
        """
        Sets the state_changed_at of this Job.


        :param state_changed_at: The state_changed_at of this Job.
        :type: int
        """

        self._state_changed_at = state_changed_at

    @property
    def finished_at(self):
        """
        Gets the finished_at of this Job.


        :return: The finished_at of this Job.
        :rtype: int
        """
        return self._finished_at

    @finished_at.setter
    def finished_at(self, finished_at):
        """
        Sets the finished_at of this Job.


        :param finished_at: The finished_at of this Job.
        :type: int
        """

        self._finished_at = finished_at

    @property
    def cpus(self):
        """
        Gets the cpus of this Job.


        :return: The cpus of this Job.
        :rtype: float
        """
        return self._cpus

    @cpus.setter
    def cpus(self, cpus):
        """
        Sets the cpus of this Job.


        :param cpus: The cpus of this Job.
        :type: float
        """

        self._cpus = cpus

    @property
    def mem(self):
        """
        Gets the mem of this Job.


        :return: The mem of this Job.
        :rtype: int
        """
        return self._mem

    @mem.setter
    def mem(self, mem):
        """
        Sets the mem of this Job.


        :param mem: The mem of this Job.
        :type: int
        """

        self._mem = mem

    @property
    def gpus(self):
        """
        Gets the gpus of this Job.


        :return: The gpus of this Job.
        :rtype: int
        """
        return self._gpus

    @gpus.setter
    def gpus(self, gpus):
        """
        Sets the gpus of this Job.


        :param gpus: The gpus of this Job.
        :type: int
        """

        self._gpus = gpus

    @property
    def image(self):
        """
        Gets the image of this Job.


        :return: The image of this Job.
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image):
        """
        Sets the image of this Job.


        :param image: The image of this Job.
        :type: str
        """

        self._image = image

    @property
    def node_selectors(self):
        """
        Gets the node_selectors of this Job.


        :return: The node_selectors of this Job.
        :rtype: str
        """
        return self._node_selectors

    @node_selectors.setter
    def node_selectors(self, node_selectors):
        """
        Sets the node_selectors of this Job.


        :param node_selectors: The node_selectors of this Job.
        :type: str
        """

        self._node_selectors = node_selectors

    @property
    def service_name(self):
        """
        Gets the service_name of this Job.


        :return: The service_name of this Job.
        :rtype: str
        """
        return self._service_name

    @service_name.setter
    def service_name(self, service_name):
        """
        Sets the service_name of this Job.


        :param service_name: The service_name of this Job.
        :type: str
        """

        self._service_name = service_name

    @property
    def external_service_name(self):
        """
        Gets the external_service_name of this Job.


        :return: The external_service_name of this Job.
        :rtype: str
        """
        return self._external_service_name

    @external_service_name.setter
    def external_service_name(self, external_service_name):
        """
        Sets the external_service_name of this Job.


        :param external_service_name: The external_service_name of this Job.
        :type: str
        """

        self._external_service_name = external_service_name

    @property
    def service_ports(self):
        """
        Gets the service_ports of this Job.


        :return: The service_ports of this Job.
        :rtype: str
        """
        return self._service_ports

    @service_ports.setter
    def service_ports(self, service_ports):
        """
        Sets the service_ports of this Job.


        :param service_ports: The service_ports of this Job.
        :type: str
        """

        self._service_ports = service_ports

    @property
    def environment(self):
        """
        Gets the environment of this Job.


        :return: The environment of this Job.
        :rtype: str
        """
        return self._environment

    @environment.setter
    def environment(self, environment):
        """
        Sets the environment of this Job.


        :param environment: The environment of this Job.
        :type: str
        """

        self._environment = environment

    @property
    def commands(self):
        """
        Gets the commands of this Job.


        :return: The commands of this Job.
        :rtype: str
        """
        return self._commands

    @commands.setter
    def commands(self, commands):
        """
        Sets the commands of this Job.


        :param commands: The commands of this Job.
        :type: str
        """

        self._commands = commands

    @property
    def project(self):
        """
        Gets the project of this Job.


        :return: The project of this Job.
        :rtype: Project
        """
        return self._project

    @project.setter
    def project(self, project):
        """
        Sets the project of this Job.


        :param project: The project of this Job.
        :type: Project
        """

        self._project = project

    @property
    def children(self):
        """
        Gets the children of this Job.


        :return: The children of this Job.
        :rtype: list[Job]
        """
        return self._children

    @children.setter
    def children(self, children):
        """
        Sets the children of this Job.


        :param children: The children of this Job.
        :type: list[Job]
        """

        self._children = children

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
