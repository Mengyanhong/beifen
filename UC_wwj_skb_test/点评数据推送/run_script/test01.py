import sys
ssh_pkey_path = sys.argv[0].split("home")[0]
print(f"{ssh_pkey_path}home/.ssh/id_rsa")