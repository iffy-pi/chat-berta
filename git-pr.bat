@echo off
rem get the repository URL
FOR /F "tokens=* USEBACKQ" %%F IN (`git config --get remote.origin.url`) DO ( SET repo_url=%%F )

rem get the current branch
FOR /F "tokens=* USEBACKQ" %%F IN (`git branch --show-current`) DO ( SET branch=%%F )

rem remove special characters to get https URL
set "repo_url=%repo_url: =%"
set "repo_url=%repo_url:.git=%"
set "repo_url=%repo_url::=/%"
set "repo_url=%repo_url:git@=https://%"
set "branch=%branch: =%"

:make_pr
echo OPENING PR LINK:
echo %repo_url%/pull/new/%branch%
start %repo_url%/pull/new/%branch%
cd %prev_dir%

:exit_script
goto :eof
