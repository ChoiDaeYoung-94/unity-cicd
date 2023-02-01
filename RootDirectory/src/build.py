import os
import shutil
import click
import paramiko
import scp
import git


@click.command()
@click.option("--user_name", prompt="Enter github user name", help="github user name (ex: ChoiDaeYoung-94)")
@click.option("--project_name", prompt="Enter github project repository name", help="github project repository name (ex: unity-cicd)")
@click.option("--branch", prompt="Enter branch name", help="branch name (ex: main)")
@click.option("--unity_app_path", prompt="Enter unity app path", help="https://docs.unity3d.com/kr/2021.3/Manual/EditorCommandLineArguments.html")
@click.option("--buildpc_project_destination_path", prompt="Enter project destination path of buildpc", help="unity project destination path in buildpc")
@click.option("--ip", prompt="Enter IPv4 of your pc", help="window > cmd > ipconfig, mac > terminal > ifconfig | grep inet")
@click.option("--username", prompt="Enter username of your pc", help="window > cmd > whoami, mac > terminal > whoami")
@click.option("--password", prompt="Enter password of your pc", help="password of your pc")
@click.option("--path", prompt="Enter path to receive build output", help="path to receive build output")
def main(user_name, project_name, branch, unity_app_path, buildpc_project_destination_path, ip, username, password, path):
    global project_url
    global project_path
    global unity_path
    global local_ip
    global local_username
    global local_password
    global local_buildpath

    project_url = f"https://github.com/{user_name}/{project_name}.git"
    project_path = f"{buildpc_project_destination_path}/{project_name}"
    unity_path = unity_app_path
    local_ip = ip
    local_username = username
    local_password = password
    local_buildpath = path

    if os.path.isdir(project_path) == False:
        click.echo(f"there is no project in {buildpc_project_destination_path} > clone {project_url}")
        git.Git(buildpc_project_destination_path).clone(project_url)

    click.echo(f"checkout {branch}")
    git.Git(project_path).checkout(branch)

    build()


def build():
    click.echo("AOS Build AAB, APK")

    click.echo("Clean Build folder")
    if os.path.isdir(f"{project_path}/Build"):
        shutil.rmtree(f"{project_path}/Build")
    os.mkdir(f"{project_path}/Build")

    click.echo("Create build log file")
    buildLogPath = f"{project_path}/Build/buildLog.txt"
    buildLogfile = open(buildLogPath, 'w')
    buildLogfile.close()

    click.echo("Build AAB - wait for build!!!!!!!!!!!!!!")
    os.system(f"{unity_path} -logFile {buildLogPath} -buildTarget Android -projectPath {project_path} -executeMethod BuildScript.BuildAOSAAB")

    output = os.listdir(f"{project_path}/Build/AOS")
    output_aab = [file for file in output if file.endswith(".aab")]
    if output_aab.count != 0:
        click.echo("AAB build success")
    else:
        click.echo(f"AAB build failed\nPlease see this log file > {buildLogPath}")
        return

    click.echo("Build APK - wait for build!!!!!!!!!!!!!!")
    os.system(f"{unity_path} -logFile {buildLogPath} -buildTarget Android -projectPath {project_path} -executeMethod BuildScript.BuildAOSAPK")

    output = os.listdir(f"{project_path}/Build/AOS")
    output_aab = [file for file in output if file.endswith(".apk")]
    if output_aab.count != 0:
        click.echo("APK build success")
    else:
        click.echo(f"APK build failed\nPlease see this log file > {buildLogPath}")
        return

    click.echo("AAB, APK build success")

    click.echo("receive build output")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=local_ip, username=local_username, password=local_password, port=22)
    sftp_client = scp.SCPClient(ssh.get_transport())

    sftp_client.put(f"{project_path}/Build", local_buildpath, recursive=True)
    sftp_client.close()
    ssh.close()
    
    click.echo("Build complete")


if __name__ == '__main__':
    main()
