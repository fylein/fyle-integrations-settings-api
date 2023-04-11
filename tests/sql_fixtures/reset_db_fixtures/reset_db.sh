#!/bin/bash

echo "-------------Populating Test Datebase---------------"
PGPASSWORD=postgres psql -h $DB_HOST -U postgres -c "drop database test_admin_settings";
PGPASSWORD=postgres psql -h $DB_HOST -U postgres -c "create database test_admin_settings";
echo "---------------------Testing-------------------------"
