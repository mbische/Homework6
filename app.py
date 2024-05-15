#!/usr/bin/env python3
import os

import aws_cdk as cdk

from homework6.homework6_stack import Homework6Stack
from homework6.homework6_network_stack import Homework6NetworkStack


app = cdk.App()

NetworkStack = Homework6NetworkStack(app, "Homework6NetworkStack")

Homework6Stack(app, "Homework6Stack", EngineeringVpc = NetworkStack.EngineeringVpc
    )


app.synth()
