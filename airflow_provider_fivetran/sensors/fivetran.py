from typing import Any, Callable, Dict, Optional

import pendulum
import logging
import json

from airflow.exceptions import AirflowException
from airflow_provider_fivetran.hooks.fivetran import FivetranHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

log = logging.getLogger(__name__)

class FivetranSensor(BaseSensorOperator):
    """
    Sensor waits for Fivetran syncs to finish.

    :param fivetran_conn_id: Maps to the id of the Connection to be used to
        configure this hook.
    :type fivetran_conn_id: str
    :param connector_id: ID of the Fivetran connector to sync, found on the
        Connector settings page.
    :type connector_id: str
    :param poke_interval: Time in seconds that the job should wait in
        between each tries
    :type poke_interval: int
    :param hook: FivetranHook that will provide interaction with Fivetran API
    :type hook: airflow_provider_fivetran.hook.FivetranHook
    :param previous_completed_at: The number of seconds to wait between retries.
    :type previous_completed_at: pendulum.datetime.DateTime
    """
    @apply_defaults
    def __init__(
        self,
        fivetran_conn_id: str = 'fivetran',
        poke_interval: int = 60,
        connector_id=None,
        hook=None,
        previous_completed_at=None,
        **kwargs: Any
    ) -> None:
        

        super().__init__(**kwargs)
        self.fivetran_conn_id = fivetran_conn_id
        self.connector_id = connector_id
        self.poke_interval = poke_interval
        self.hook = FivetranHook(self.fivetran_conn_id)
        self.previous_completed_at = self.hook.get_last_sync(self.connector_id)


    def poke(self, context):
       return self.hook.get_sync_status(self.connector_id, self.previous_completed_at)


 
