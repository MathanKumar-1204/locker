-- Reset PostgreSQL Database for Locker System
-- Run this in Supabase SQL Editor or psql

-- Drop all tables in correct order (to handle foreign keys)
DROP TABLE IF EXISTS reservations_reservation CASCADE;
DROP TABLE IF EXISTS lockers_locker CASCADE;
DROP TABLE IF EXISTS accounts_admin CASCADE;
DROP TABLE IF EXISTS accounts_user CASCADE;

-- Drop Django system tables
DROP TABLE IF EXISTS django_admin_log CASCADE;
DROP TABLE IF EXISTS django_content_type CASCADE;
DROP TABLE IF EXISTS auth_permission CASCADE;
DROP TABLE IF EXISTS auth_group CASCADE;
DROP TABLE IF EXISTS django_migrations CASCADE;
DROP TABLE IF EXISTS django_session CASCADE;

-- Now you can run: python manage.py migrate
