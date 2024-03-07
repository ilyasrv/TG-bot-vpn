

from yoomoney import Client
token = "4100117853537949.83A3FB772A51B28DB1A367CE946AB11E68E3EEEBC7AD86C0601BAFFBC739F0DC051674F31EDC39F79BECE6E2154D205E1A3FB3B936A3A0BF44BCB06A68C277217CE82BEEB90DB947763D5F43B411CB9C1A8638260B0B995AE0C2D0555AF21F19518DB340ED7B3F1CF240763CAA7ACD7FF6D3B317F578AB39F9B4F4C89C5F0E8C"
client = Client(token)
history = client.operation_history(label="a1b2c3d4e5")
print("List of operations:")
print("Next page starts with: ", history.next_record)
for operation in history.operations:
    print()
    print("Operation:",operation.operation_id)
    print("\tStatus     -->", operation.status)
    print("\tDatetime   -->", operation.datetime)
    print("\tTitle      -->", operation.title)
    print("\tPattern id -->", operation.pattern_id)
    print("\tDirection  -->", operation.direction)
    print("\tAmount     -->", operation.amount)
    print("\tLabel      -->", operation.label)
    print("\tType       -->", operation.type)