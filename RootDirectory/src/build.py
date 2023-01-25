import os
import click
import git


@click.command()
@click.option("--user_name", prompt="Enter github user name", help="github user name (ex: ChoiDaeYoung-94)")
@click.option("--project_name", prompt="Enter github project repository name", help="github project repository name (ex: unity-cicd)")
@click.option("--branch", prompt="Enter branch name", help="branch name (ex: main)")
@click.option("--unity_app_path", prompt="Enter unity app path", help="https://docs.unity3d.com/kr/2021.3/Manual/EditorCommandLineArguments.html")
@click.option("--buildpc_projects_path", prompt="Enter projects path of buildpc", help="unity projects path in buildpc")
def main(user_name, project_name, branch, unity_app_path, buildpc_projects_path):
    global project_url
    global project_path
    global unity_path

    project_url = f"https://github.com/{user_name}}/{project_name}.git"
    project_path = f"{buildpc_projects_path}/{project_name}"
    unity_path = unity_app_path

    if os.path.isdir(project_path) == False:
        click.echo(f"there is no project > clone {project_url}")
        git.Git(buildpc_projects_path).clone(project_url)

    click.echo(f"checkout {branch}")
    git.Git(project_path).checkout(branch)

    build()


def build():
    click.echo("AOS Build AAB, APK")

    os.system(
        f"{unity_path} -buildTarget Android -projectPath {project_path} -executeMethod BuildScript.BuildAOSAAB")
    os.system(
        f"{unity_path} -buildTarget Android -projectPath {project_path} -executeMethod BuildScript.BuildAOSAPK")


if __name__ == '__main__':
    main()
