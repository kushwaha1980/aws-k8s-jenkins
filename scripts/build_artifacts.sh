#!/bin/sh -e
LAMBDA_DEPS_ZIP_FILE="lambda.zip"
LAMBDA_DEPS_ZIP_FILE_NAME=$(echo $LAMBDA_DEPS_ZIP_FILE | cut -d'.' -f 1)
create_lambda_dependents_zip() {
    echo "Building lambda package for Enforce Tag repo"
    files_to_include_in_root="functions/*.*"
    base_path=$(pwd)
    packge_dir="__lambda_package__"
    # Cleanup package directory
    rm -rf $packge_dir
    mkdir $packge_dir
    # Copy files to root location
    for file in $files_to_include_in_root; do
        cp $file $packge_dir/
    done
    cp ${base_path}/enforce_config.yaml $packge_dir/
    cp ${base_path}/config.yml $packge_dir/
    # echo "Installing dependencies into local pip env dir"
    cd $packge_dir
    python3 -m pip install pyyaml boto3 requests -t .
    python3 -m pip install -r requirements.txt -t ./
    # Remove dist-info & __pycache__ & .pyc files
    rm -r *.dist-info || true
    find . \( -name __pycache__ -o -name "*.pyc" \) -delete
    chmod -R 0755 *
    zip -r9 ${base_path}/terraform/${LAMBDA_DEPS_ZIP_FILE} .
    # Get out of packge_dir
    cd ..
    # Cleanup
    rm -rf $packge_dir
    cd "${base_path}"
}
#copy_profile_yaml() {
#    base_path=$(pwd)
#    source_path="${base_path}/flute/profiles/profiles.yaml"
#    dest_path="${base_path}/terraform/"
#
#    echo "Copying ${source_path} to ${dest_path}"
#    cp $source_path $dest_path
#}
# Call funcs
create_lambda_dependents_zip
# Copy profiles.yaml to terraform
# copy_profile_yaml