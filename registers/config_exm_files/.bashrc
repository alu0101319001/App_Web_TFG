# /home/modo_examen/.bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# User specific aliases and functions
alias ll='ls -l'
alias la='ls -A'
alias l='ls -CF'

# Custom prompt
PS1='\u@\h:\w\$ '

# Custom environment variables
export EXAM_MODE=true

# Run a custom script at login (optional)
if [ -x /home/modo_examen/exam_login_script.sh ]; then
    /home/modo_examen/exam_login_script.sh
fi
