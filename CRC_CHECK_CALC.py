#-------------------------------------------------------------------------------
# Name:        CRC_CHECK_CALC
# Purpose:
#
# Author:      U560764
#
# Created:     20/08/2019
# Copyright:   (c) U560764 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def crc(msg, div, code='11111111'):
    """Cyclic Redundancy Check
    Generates an error detecting code based on an inputted message
    and divisor in the form of a polynomial representation.
    Arguments:
        msg: The input message of which to generate the output code.
        div: The divisor in polynomial form. For example, if the polynomial
            of x^3 + x + 1 is given, this should be represented as '1011' in
            the div argument.
        code: This is an option argument where a previously generated code may
            be passed in. This can be used to check validity. If the inputted
            code produces an outputted code of all zeros, then the message has
            no errors.
    Returns:
        An error-detecting code generated by the message and the given divisor.
    """
    # Append the code to the message. If no code is given, default to '1111111'
    # Uncomment every occurence of msg_XORIN if not CRC-8 SAE J1850
    msg_XORIN = [] # XOR the input before appending the code
    msg_XORIN = [str((int(msg[i])+1) %2) for i in range(len(list(msg)))]
    msg = msg_XORIN

    div = list(div)
    msg = list(msg) + list(code) # Convert msg and div into list form for easier handling

    # Loop over every message bit (minus the appended code)
    for i in range(len(msg)-len(code)):
        # If that messsage bit is not one, shift until it is.
        if msg[i] == '1':
            for j in range(len(div)):
                # Perform modulo 2 ( == XOR) on each index of the divisor
                msg[i+j] = str((int(msg[i+j])+int(div[j]))%2)

    # Output the last error-checking code portion of the message generated

    return ''.join(msg[-len(code):])