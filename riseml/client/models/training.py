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


class Training(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, id=None, short_id=None, state=None, state_changed_at=None, created_at=None, started_at=None, finished_at=None, framework=None, framework_details=None, image=None, run_commands=None, active_job_count=None, jobs=None, changeset=None, runs=None):
        """
        Training - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'short_id': 'int',
            'state': 'str',
            'state_changed_at': 'int',
            'created_at': 'int',
            'started_at': 'int',
            'finished_at': 'int',
            'framework': 'str',
            'framework_details': 'TrainingFrameworkDetails',
            'image': 'str',
            'run_commands': 'list[str]',
            'active_job_count': 'int',
            'jobs': 'list[Job]',
            'changeset': 'Changeset',
            'runs': 'list[Run]'
        }

        self.attribute_map = {
            'id': 'id',
            'short_id': 'short_id',
            'state': 'state',
            'state_changed_at': 'state_changed_at',
            'created_at': 'created_at',
            'started_at': 'started_at',
            'finished_at': 'finished_at',
            'framework': 'framework',
            'framework_details': 'framework_details',
            'image': 'image',
            'run_commands': 'run_commands',
            'active_job_count': 'active_job_count',
            'jobs': 'jobs',
            'changeset': 'changeset',
            'runs': 'runs'
        }

        self._id = id
        self._short_id = short_id
        self._state = state
        self._state_changed_at = state_changed_at
        self._created_at = created_at
        self._started_at = started_at
        self._finished_at = finished_at
        self._framework = framework
        self._framework_details = framework_details
        self._image = image
        self._run_commands = run_commands
        self._active_job_count = active_job_count
        self._jobs = jobs
        self._changeset = changeset
        self._runs = runs


    @property
    def id(self):
        """
        Gets the id of this Training.


        :return: The id of this Training.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Training.


        :param id: The id of this Training.
        :type: str
        """

        self._id = id

    @property
    def short_id(self):
        """
        Gets the short_id of this Training.


        :return: The short_id of this Training.
        :rtype: int
        """
        return self._short_id

    @short_id.setter
    def short_id(self, short_id):
        """
        Sets the short_id of this Training.


        :param short_id: The short_id of this Training.
        :type: int
        """

        self._short_id = short_id

    @property
    def state(self):
        """
        Gets the state of this Training.


        :return: The state of this Training.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this Training.


        :param state: The state of this Training.
        :type: str
        """

        self._state = state

    @property
    def state_changed_at(self):
        """
        Gets the state_changed_at of this Training.


        :return: The state_changed_at of this Training.
        :rtype: int
        """
        return self._state_changed_at

    @state_changed_at.setter
    def state_changed_at(self, state_changed_at):
        """
        Sets the state_changed_at of this Training.


        :param state_changed_at: The state_changed_at of this Training.
        :type: int
        """

        self._state_changed_at = state_changed_at

    @property
    def created_at(self):
        """
        Gets the created_at of this Training.


        :return: The created_at of this Training.
        :rtype: int
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """
        Sets the created_at of this Training.


        :param created_at: The created_at of this Training.
        :type: int
        """

        self._created_at = created_at

    @property
    def started_at(self):
        """
        Gets the started_at of this Training.


        :return: The started_at of this Training.
        :rtype: int
        """
        return self._started_at

    @started_at.setter
    def started_at(self, started_at):
        """
        Sets the started_at of this Training.


        :param started_at: The started_at of this Training.
        :type: int
        """

        self._started_at = started_at

    @property
    def finished_at(self):
        """
        Gets the finished_at of this Training.


        :return: The finished_at of this Training.
        :rtype: int
        """
        return self._finished_at

    @finished_at.setter
    def finished_at(self, finished_at):
        """
        Sets the finished_at of this Training.


        :param finished_at: The finished_at of this Training.
        :type: int
        """

        self._finished_at = finished_at

    @property
    def framework(self):
        """
        Gets the framework of this Training.


        :return: The framework of this Training.
        :rtype: str
        """
        return self._framework

    @framework.setter
    def framework(self, framework):
        """
        Sets the framework of this Training.


        :param framework: The framework of this Training.
        :type: str
        """

        self._framework = framework

    @property
    def framework_details(self):
        """
        Gets the framework_details of this Training.


        :return: The framework_details of this Training.
        :rtype: TrainingFrameworkDetails
        """
        return self._framework_details

    @framework_details.setter
    def framework_details(self, framework_details):
        """
        Sets the framework_details of this Training.


        :param framework_details: The framework_details of this Training.
        :type: TrainingFrameworkDetails
        """

        self._framework_details = framework_details

    @property
    def image(self):
        """
        Gets the image of this Training.


        :return: The image of this Training.
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image):
        """
        Sets the image of this Training.


        :param image: The image of this Training.
        :type: str
        """

        self._image = image

    @property
    def run_commands(self):
        """
        Gets the run_commands of this Training.


        :return: The run_commands of this Training.
        :rtype: list[str]
        """
        return self._run_commands

    @run_commands.setter
    def run_commands(self, run_commands):
        """
        Sets the run_commands of this Training.


        :param run_commands: The run_commands of this Training.
        :type: list[str]
        """

        self._run_commands = run_commands

    @property
    def active_job_count(self):
        """
        Gets the active_job_count of this Training.


        :return: The active_job_count of this Training.
        :rtype: int
        """
        return self._active_job_count

    @active_job_count.setter
    def active_job_count(self, active_job_count):
        """
        Sets the active_job_count of this Training.


        :param active_job_count: The active_job_count of this Training.
        :type: int
        """

        self._active_job_count = active_job_count

    @property
    def jobs(self):
        """
        Gets the jobs of this Training.


        :return: The jobs of this Training.
        :rtype: list[Job]
        """
        return self._jobs

    @jobs.setter
    def jobs(self, jobs):
        """
        Sets the jobs of this Training.


        :param jobs: The jobs of this Training.
        :type: list[Job]
        """

        self._jobs = jobs

    @property
    def changeset(self):
        """
        Gets the changeset of this Training.


        :return: The changeset of this Training.
        :rtype: Changeset
        """
        return self._changeset

    @changeset.setter
    def changeset(self, changeset):
        """
        Sets the changeset of this Training.


        :param changeset: The changeset of this Training.
        :type: Changeset
        """

        self._changeset = changeset

    @property
    def runs(self):
        """
        Gets the runs of this Training.


        :return: The runs of this Training.
        :rtype: list[Run]
        """
        return self._runs

    @runs.setter
    def runs(self, runs):
        """
        Sets the runs of this Training.


        :param runs: The runs of this Training.
        :type: list[Run]
        """

        self._runs = runs

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
