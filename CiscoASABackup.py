import logging
import pathlib
import asyncio
import paramiko
import os

# Use environment variables to get sensitive information
username = os.environ.get('SSH_USERNAME')
private_key_passphrase = os.environ.get('SSH_PRIVATE_KEY_PASSPHRASE')

class SSHClient:
    def __init__(self, host, username, private_key_path, commands):
        self.host = host
        self.username = username
        self.private_key_path = private_key_path
        self.commands = commands
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    async def connect(self):
        await asyncio.sleep(0)
        # Use password authentication instead of private key authentication
        self.client.connect(self.host, username=self.username, password=private_key_passphrase)

    async def send_command(self):
        await self.connect()
        async with self.client.invoke_shell() as shell:
            for command in self.commands:
                shell.send(command)
                await asyncio.sleep(0.1)
            output = ''
            while not shell.exit_status_ready():
                if shell.recv_ready():
                    output += shell.recv(4096).decode()
                    await asyncio.sleep(0.1)
            output += shell.recv(4096).decode()
            await asyncio.sleep(0.1)
        self.client.close()
        return output


async def main():
    hosts = [
        'dev0',
        'dev1'
    ]

    # Use a configuration file or a database to store hostnames and commands
    with open('config.txt', 'r') as f:
        config = f.readlines()

    commands = []
    for line in config:
        if line.startswith('#'):
            continue
        commands.append(line.strip())

    tasks = []
    for host in hosts:
        ssh_client = SSHClient(host, username, private_key_path, commands)
        tasks.append(asyncio.create_task(ssh_client.send_command()))

    outputs = await asyncio.gather(*tasks)

    config_dir_path = pathlib.Path.home() / 'output' / pathlib.Path(f"{datetime.datetime.now().strftime('%Y%m%d')}")
    config_dir_path.mkdir(parents=True, exist_ok=True)

    for host, output in zip(hosts, outputs):
        with open(config_dir_path / f"{host.upper()}.txt", 'w') as f:
            f.write(output)
            logging.info(f"Configuration for {host} written to {config_dir_path}/{host.upper()}.txt")


if __name__ == '__main__':
    logging.basicConfig(filename=f"{pathlib.Path.home()}/output.log", level=logging.INFO)

    # Use SSH agent forwarding
    ssh_agent = paramiko.Agent()
    private_keys = ssh_agent.get_keys()
    if len(private_keys) > 0:
        private_key_path = private_keys[0].filename
    else:
        raise Exception("No private key found in SSH agent")

    asyncio.run(main())
