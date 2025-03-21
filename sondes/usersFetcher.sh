#!/bin/bash

user_count=$(who | wc -l)

# Retourner un objet JSON
echo "{\"USERS\": \"$user_count\"}"
