import configparser


def save_history_to_config(history, file_path):
    history_config = configparser.ConfigParser()
    if not history_config.has_section('History'):
        history_config.add_section('History')
    history_config.set('History', 'numbers', ','.join(map(str, history)))
    with open(file_path, 'w') as configfile:
        history_config.write(configfile)


def retrieve_history_from_config(file_path):
    history_config = configparser.ConfigParser()
    history_config.read(file_path)
    history_numbers = []
    if 'History' in history_config:
        history_numbers = history_config['History'].get('numbers', '').split(',')
    return list(map(int, history_numbers))


class SecretsManager:
    def __init__(self, secret_file):
        self.secret_config = configparser.ConfigParser()
        self.secret_config.read(secret_file)

    def get_secrets(self):
        secrets = {
            'user': self.secret_config.get('secrets', 'user'),
            'password': self.secret_config.get('secrets', 'password'),
            'dsn': self.secret_config.get('secrets', 'dsn'),
            'config_dir': self.secret_config.get('secrets', 'config_dir'),
            'wallet_location': self.secret_config.get('secrets', 'wallet_location'),
            'wallet_password': self.secret_config.get('secrets', 'wallet_password')
        }
        return secrets
