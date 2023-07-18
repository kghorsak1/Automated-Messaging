# Automated-Messaging
I created this as a passion project inspired by real issues within a local company. The goal was to automate the messaging/communication process between this business's employees and customers

Context: My best friend, Carlo Domingo, serves as the Austin Manager for Texas Kayak Tours and since he started (May 2022) has always complained about how their messaging system works (ie they dont have one).This was created over the span of 1-2 months during the spring semester of my junior year. This truly was a passion project as this was done on my own accord while having a full course load and working part time at an MEP firm.

The Problem: Employees at Texas Kayak Tours give multiple tours a day and these tours can range from 1-30+ people. The tour guide sends an individual copy and pasted text to each of these customers and has to deal with up to 50+ message threads a day from their personal device. 

The 3-Step Solution: 1. Use a chromedriver and login creditials to access a site that we want to webscrape useful customer info from. 2. Organize and manipulate that data into a prefered format 3. Connecting to the Twilio API and sending the script the tour guide would other wise have to send

Output: I have an amazon EC2 instance up and runnning where I can activate this code at any time to send daily messages to my friends and respond to them all within one message thread

Dependencies: Scheduling website is FareHarbor.com. Have access to a Twilio Messaging API. Runs on an free Amazon EC2 instance in perpentuity.

Limits: Due to A2P restrictions, messages send via the Twilio API are capped at 160 characters and links cannot be sent
