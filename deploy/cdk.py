from aws_cdk import App

from fastapi import BusObservatoryAPI_FastAPIStack

app = App()

BusObservatoryAPI_FastAPIStack(app, "BusObservatoryAPI_FastAPIStack")
app.synth()
