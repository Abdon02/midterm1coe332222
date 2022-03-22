import app
import pytest 
from flask import Flask, request, jsonify

#Testing the function that prints out the welcome message 
def test_welcome_message():
    assert isinstance(app.welcome_message(), str) == True


    
