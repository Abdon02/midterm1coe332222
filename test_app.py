from app import welcome_message
import pytest 
from flask import Flask, request, jsonify

#Testing the function that prints out the welcome message 
def test_welcome_message():
    assert isinstance(welcome_message(), str) == True
