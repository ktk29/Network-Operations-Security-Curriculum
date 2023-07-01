import subprocess

#function which takes the target computer's username and IP address
def send_file(username, ip):
    # Creating a "Hello World" txt file
    file_content = "Hello, World!"
    with open("hello.txt", "w") as file:
        file.write(file_content)

    # Sending the file to target using SCP
    subprocess.run(["scp", "hello.txt", f"{username}@{ip}:~/hello.txt"])

    # Taking remote access of targer using SSH
    ssh_command = f"ssh {username}@{ip} 'cd ~; ls; chmod a+rw hello.txt'"
    subprocess.run(ssh_command, shell=True)
