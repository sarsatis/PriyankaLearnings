import requests

import json

import os

import yaml

from github import Github

from github.GithubException import UnknownObjectException, GithubException

import urllib3

from requests.exceptions import ReadTimeout

import socket

import tempfile

import fileinput




class CreatePRAndAddLabel:

   

    API_TOKEN = os.getenv('GITHUB_TOKEN_PSW')

    num_retries = 10

    backoff_factor = 15

    retry_data = urllib3.util.retry.Retry(total=num_retries,read=num_retries,connect=num_retries,backoff_factor=backoff_factor,)

    github_client = Github(base_url="https://ghe.service.group/api/v3",login_or_token=os.getenv('GITHUB_TOKEN_PSW'), retry=retry_data)

    app_name = os.getenv('appName')

    application_manifest_repo = "helm-charts-ocp"

    build_id = os.getenv('BUILD_ID')

    branch_name = os.getenv('GIT_BRANCH')

    print(branch_name)

    file_path = f"manifests/{app_name}/sit/immutable/values-sit.yaml"

    git_commit_prefix = "feat"

    image_tag = os.getenv('buildahImageTag')

    # label_headers = {

    #     'Accept': 'application/vnd.github+json',

    #     'Authorization': authorization,

    #     'Content-Type': 'application/json',

    # }




    # label_data = {

    #     "labels": [name,"dev"]

    # }

    errored_messages = []

    repo = ""




    def __init__(self):

        print("inside Init")

        self.create_pull_requests()





    def create_pull_requests(self):

        try:

            print("inside PR")

            repo = self.github_client.get_organization("devops-pipelines").get_repo(self.application_manifest_repo)

            print(f"repo details {repo}")

        except UnknownObjectException:

            error = f"[SKIPPING] Repo doesn't exist or have no access-{self.application_manifest_repo}"

            self.errored_messages.append(error)

            print(error)

       

        if repo.archived:

            print(f"[SKIPPING] Archived repo - {self.application_manifest_repo}")

           

        file_content = repo.get_contents(self.file_path, ref=repo.default_branch)




        update_file = False

        branch_created = False

        for pr in repo.get_pulls():

            if self.branch_name == pr.head.ref:

                try:

                    file_content = repo.get_contents(self.file_path, ref=pr.head.ref)

                    # update_file = True

                    branch_created = True

                except UnknownObjectException:

                    print(f"[INFO] File wasn't found")

                    file_content_decoded = ""




       

        file_content_decoded = file_content.decoded_content.decode()

        print(file_content_decoded)    

        new_file_content = getattr(self, "update_file")(file_content=file_content_decoded, file_name="values-sit.yaml", variable_key = "imageTag")

        print(new_file_content)




        git_method = "update_file"

        git_method_args = {

            "content":new_file_content,

            "path":self.file_path,

            "branch":self.branch_name,

            "message":f"{self.git_commit_prefix}: {self.branch_name} - Upadting image tag for application {self.app_name}",

            "sha": file_content.sha

        }




        # if update_file:

        #     git_method_args['sha'] = file_content.sha

        #     git_method="update_file"




        if not branch_created:

            try:

                repo_branch = repo.get_branch(repo.default_branch)

                repo.create_git_ref(ref=f'refs/heads/{self.branch_name}', sha=repo_branch.commit.sha)

                branch_created = True

            except UnknownObjectException as e:

                if "Not Found" in e.data['message']:

                    err = f"[SKIPPING] {repo.name} - branch unable to be created - most likely due to permissions or empty repo"

                    print(err)

                    self.errored_messages.append(err)





        getattr(repo, git_method)(**git_method_args)




        title = f"{self.git_commit_prefix}: {self.branch_name} - Update image tag for application {self.app_name}"




        try:

            pr = repo.create_pull(head=self.branch_name,base=repo.default_branch,title=title,body=title)

        except (GithubException, socket.timeout, urllib3.exceptions.ReadTimeoutError, ReadTimeout) as e:

            print(f"PR creation timeout - ({repo.name}) - sleeping 60s")

            print(f"Details: {e}")

       

       





    @staticmethod

    def update_file(**kwargs):

        content = kwargs['file_content']

        print(content)

        if not content:

            return ""

        tmp = tempfile.NamedTemporaryFile()

        # Open the file for writing.

        with open(tmp.name, 'w') as f:

            yaml.dump(content, f, default_flow_style=False, allow_unicode=True)




        # Read YAML file

        with open(tmp.name, 'r') as stream:

            data_loaded = yaml.safe_load(stream)

            print(data_loaded)

           

       

        for kwargs['variable_key'] in fileinput.input(tmp.name, inplace=True):

            print('{} {}'.format(fileinput.filelineno(), f"{kwargs['variable_key']}: {os.getenv('buildahImageTag')}"), end='') # for Python 3

        # # read through file and perform replacement

        # content_lines = content.split("\n")

        # i = 0

       

        # while i < len(content_lines):

        #     print(f"variable key {kwargs['variable_key']}")

        #     print(f"content_lines {content_lines}")

        #     if content_lines[i].split(':')[0] == kwargs["variable_key"]:

        #         print(f"Update line content {content_lines[i]}")

        #         print(f"Update line content {content_lines[i].split(':')[0]}")

        #         content_lines[i] = f"{kwargs['variable_key']}: {os.getenv('buildahImageTag')}"

        #     i +=1

        # content = "\n".join(content_lines)

        # content = "\n".join(list(content.splitlines()))

        return content




    @staticmethod

    def pretty_pr_url(url):

        return url.replace("api.ghe.service.group/repos/", "ghe.service.group/").replace("/pulls/", "/pull/")

           




   

    def label_pull_requests(self, pr_number):

        print('https://ghe.service.group/devops-pipelines/helm-charts-ocp/issues/{pr_number}/labels')

        response = requests.post(f'https://ghe.service.group/devops-pipelines/helm-charts-ocp/issues/{pr_number}/labels', headers=self.label_headers, data=json.dumps(self.label_data))

        print(response)




if __name__ == "__main__":

    CreatePRAndAddLabel()
