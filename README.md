# Text Based Occupation Classification

## Introduction

This repo holds a classification method for classifying occupational strings to a set of different schemas.

This is part of my PhD project on technological change in Sweden in the 20th century.

This is ongoing work and the code is not yet finished, check back later.

## Planning

The approach to classify occupations as recorded in biographical dictionaries is relatively simple.

We have a schema of occupations grouped into different sectors. Each occupation has a description of the tasks and duties involved with the occupation. One popular schema is HISCO. Another is ISCO. We take these titles and descriptions and project them into a vector space using a text embedding model (sentence and word - we need to see which works better). 

Then we take the occupational strings and use the same text embedding model to project them into a vector space. 

To classify the occupational strings according to the schema, we calculate the distance between the string and it's closest occupation in the schema from the schema. We set some threshold whereby it is deemed a close enough match, and classify the string as that occupation.

## Data

We are gathering schemas from HISCO and ISCO. 