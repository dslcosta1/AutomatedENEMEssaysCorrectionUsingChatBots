echo "### Preparing virtual envitonment ###"
python3 -m venv venv
source venv/bin/activate

echo "### Checking dependencies and configurations ###"
pip install -r requirements.txt

pip install -U -q google-generativeai

git config filter.strip-notebook-output.clean "jupyter nbconvert --ClearOutputPreprocessor.enabled=True --ClearMetadataPreprocessor.enabled=True --to=notebook --stdin --stdout --log-level=ERROR"

echo "### Running Jupyter Lab ###"
jupyter lab