# Text Based Occupation Classification

## Introduction

This repo holds a classification method for classifying occupational
strings to a set of different schemas.

This is part of my PhD project on technological change in Sweden in the
20th century.

This is ongoing work and the code is not yet finished, check back later.

## Planning

The approach to classify occupations as recorded in biographical
dictionaries is relatively simple.

We have a schema of occupations grouped into different sectors. Each
occupation has a description of the tasks and duties involved with the
occupation. One popular schema is HISCO. Another is ISCO. We take these
titles and descriptions and project them into a vector space using a
text embedding model (sentence and word - we need to see which works
better).

Then we take the occupational strings and use the same text embedding
model to project them into a vector space.

To classify the occupational strings according to the schema, we
calculate the distance between the string and it’s closest occupation in
the schema from the schema. We set some threshold whereby it is deemed a
close enough match, and classify the string as that occupation.

## Data

We are gathering schemas from HISCO and ISCO to begin with at different
levels of specificity.

For example, a HISCO code can be 5 digits long.

## Assign HISCOs: process

``` mermaid
graph TB
    A[Collect HISCO Codes&lt;br&gt;and Descriptions] --&gt;|Use OpenAI API| B[Convert HISCO Titles&lt;br&gt;and Descriptions to Vectors]
    C[Receive Occupational&lt;br&gt;Strings] --&gt;|Use OpenAI API| D[Convert Occupational&lt;br&gt;Strings to Vectors]
    B --&gt; E[Compare Vectors in&lt;br&gt;Vector Space]
    D --&gt; E
    E --&gt; F[Assign HISCO Code to&lt;br&gt;Occupational String&lt;br&gt;using Cosine Distance]
    style A fill:#2B8CBE
    style B fill:#be5d2b
    style C fill:#2B8CBE
    style D fill:#be5d2b
    style E fill:#6f6fbf
    style F fill:#F4FA58


```
