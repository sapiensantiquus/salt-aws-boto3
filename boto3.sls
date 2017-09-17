python-pip:
  pkg.installed

boto3:
  pip.installed:
    - name: boto3
    - reload_modules: True
    - require:
      - pkg: python-pip
