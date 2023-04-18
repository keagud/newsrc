VENV_TMP="/tmp/newsrc_venv/"
python3 -m venv $VENV_TMP

PIPENV="$VENV_TMP/bin/pip"

$PIPENV install -r requirements.txt

$VENV_TMP/bin/shiv -c newsrc $( cat requirements.txt ) -o ~/.local/bin/newsrc  .


TEMPLATE_DIR="$HOME/.local/templates/newsrc"

if [[ ! -d  $TEMPLATE_DIR ]]; then
    mkdir -p $TEMPLATE_DIR
    cp ./templates/* $TEMPLATE_DIR/
fi

rm -rf $VENV_TMP





