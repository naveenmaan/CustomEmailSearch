import os
import yaml


class Config:

    @staticmethod
    def get_config():
        """
        method to get the config from the config file
        :return: {"connection": {"host": "localhost"}}
        """

        mode = os.getenv("MODE")

        with open(f"./config/config_{mode.lower()}.yaml", "r") as config_file:
            config = yaml.safe_load(config_file)

        return config
