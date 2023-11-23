# VideoUploader
A horrible Video Uploader for GitHub.

I created this uploader a while back, so I decided to upload this now.
This isn't really useful to me as GitHub now has a file cap of 30 or 40mb.


## Installation
You need to install the [PyGitHub](https://github.com/PyGithub/PyGithub) and [PyYAML](https://pypi.org/project/PyYAML/) package for the code to work. 
```bash
pip install PyGithub PyYAML
```

## Configuration
For the uploader to work succesfully, you need to fill out the config.yml

```YML
github_token: <Your GitHub Token>
repository_name: <Your GitHub Repo>
```


## Setup
!!! Please make sure not to leak your GitHub token to anyone as it could give access to your GitHub account. !!!
To get your token, go to:
Settings > Developer Settings > Tokens (classic) > Generate new token > Generate new token (classic)

Paste your token in ```<Your GitHub Token>``` and create a repository on GitHub and copy the name onto ```<Your GitHub Repo>```.


## Credits
[Cryzis](https://cryzis.uk)

You are welcome to use my code, though this is licensed with MIT.
