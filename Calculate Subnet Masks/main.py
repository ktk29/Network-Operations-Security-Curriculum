def bitOperations(subnet_mask, ip):
    subnet_address = []
    broadcast = []

    for i in range(4):
        subnet_address.append(subnet_mask[i] & ip[i])
        broadcast.append(subnet_address[i] | (~subnet_mask[i] + 256))

    return subnet_address, broadcast


def getSubnetMask(cidr):
    nums = []

    # make all the bits 1
    for i in range(cidr // 8):
        nums.append(255)

    remaining = 0
    for j in range(7, 7 - cidr % 8, -1):
        remaining += 2 ** j
    nums.append(remaining)

    for k in range(4 - len(nums), 0, -1):
        nums.append(0)

    return nums


def printOutput(subnet, broadcast):
    broadcastAddress = ""
    subnetAddress = ""
    minValue = ""
    maxValue = ""

    for i in range(4):
        if i == 3:
            minValue = subnetAddress + str(subnet[i] + 1)
            maxValue = broadcastAddress + str(broadcast[i]-1)

        subnetAddress += str(subnet[i]) + "."
        broadcastAddress += str(broadcast[i]) + "."

    print("The broadcast address is: " + broadcastAddress[:-1])
    print("The subnet address is: " + subnetAddress[:-1])
    print("The valid host range is: " + minValue + " to " + maxValue)


if __name__ == '__main__':
    ip_cidr = input("Please enter an IP address and its corresponding subnet mask in CIDR notation: ")
    cidr = int(ip_cidr[ip_cidr.find("/") + 1:])
    ip = ip_cidr[0:ip_cidr.find("/")]
    ip_nums = ip.split(".")
    for i in range(len(ip_nums)):
        ip_nums[i] = int(ip_nums[i])
    subnet, broadcast = bitOperations(getSubnetMask(cidr), ip_nums)
    printOutput(subnet, broadcast)
