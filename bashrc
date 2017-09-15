# source this from your .bashrc for fun

alias super='sudo /deathops/ve/bin/supervisorctl -c /deathops/src/init/supervisord.conf -s unix:///deathops/run/supervisord.sock'
alias dve='source /deathops/ve/bin/activate'

export PYTHONIOENCODING="utf-8"
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="UTF-8"
export LANG="en_US.UTF-8"
