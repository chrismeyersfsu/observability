"""Independent of OTEL things."""

import os
import sys


class ObservabilityConfig:
    """Extra meta-data"""
    def __init__(
        self,
        service_name: str = None,
        instance_name: str = None,
    ) -> None:
        """Properties that will be added to every log message.

        :param service_name: name of the process
        :param instance_id: host name
        """

        self.service_name = service_name or self.generate_service_name()
        self.instance_id = instance_id or os.uname().nodename

    def generate_service_name(self):
        """Create service name from process name."""

        # TODO: Push the service name down
        return sys.argv[1] if len(sys.argv) > 1 else (
            sys.argv[0] or 'unknown_service')
