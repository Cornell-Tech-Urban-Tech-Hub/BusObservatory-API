from aws_cdk import App

from stack import BusObservatoryAPI

app = App()

BusObservatoryAPI(app, "BusObservatoryAPI-Containerized")
app.synth()
