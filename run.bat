@echo off

start cmd /k "py -3.12 run.py & timeout /t 1 & exit"

@echo on