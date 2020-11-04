#!/usr/bin/env bash

shell="${SHELL}"
PYENV_ROOT="${HOME}/.pyenv"
IFS='/'
read -a strarr <<< "$shell"
length=${#strarr[*]}
shell=${strarr[$length-1]} 
IFS=' '

echo "Sh3ll is: ${shell}" >&1

case "$shell" in
bash )
profile="~/.bashrc"
;;
sh )
profile="~/.profile"
;;
zsh )
profile="~/.zshrc"
;;
ksh )
profile="~/.profile"
;;
fish )
profile="~/.config/fish/config.fish"
;;
* )
profile="your profile"
;;
esac

echo "Profile is: ${profile}" >&1
PROFILE=${HOME}/${profile#'~/'}
echo "Expanded correct PROFILE is: ${PROFILE}" >&1

case "$shell" in
fish )
	PATH_LINE=("set -x PATH \"$PYENV_ROOT/bin\" \$PATH" "status --is-interactive; and . (pyenv init -|psub)" "status --is-interactive; and . (pyenv virtualenv-init -|psub)")
  ;;
* )
  	PATH_LINE=("export PATH=\"$PYENV_ROOT/bin:\$PATH\"" "eval \"\$(pyenv init -)\"" "eval \"\$(pyenv virtualenv-init -)\"")
  ;;
esac

for line in "${PATH_LINE[@]}"
do
	grep "$line" "$PROFILE" >> /dev/null
	if [ $? != 0 ]; then
		{
			echo "Adding \"${line}\" to Path..."
			echo "$line" >> "$PROFILE"
		}
	fi
done

echo "Pyenv is in Path"
