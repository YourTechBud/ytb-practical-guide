## Prerequistes

**Ensure Local Database & Prod Database Schemas Are In Sync**. We are using the below schema for our local & prod dbs 👇

```
create table trainer (id serial, name varchar(100), city varchar(100), primary key (id));

create table pokemon (id serial, name varchar(100), power int, caught_on timestamp, trainer_id int, primary key (id), foreign key (trainer_id) references trainer(id));
```


## Step 1. Generate Inital Migration File From Local DB

```
export DATABASE_URL="postgresql://postgres:mysecretpassword@localhost:5435/postgres?schema=local"

npx prisma migrate diff --from-empty --to-url "$DATABASE_URL" --script > migration.sql 
```

## Step 2. Create Required Directory Structure Of Prisma

```
mkdir -p prisma/migrations/v1.0.0

mv migration.sql prisma/migrations/v1.0.0

touch prisma/migrations/migration_lock.toml

echo 'provider = "postgresql"' >> prisma/migrations/migration_lock.toml

touch prisma/schema.prisma

echo 'datasource db {
    provider = "postgresql"
    url      = env("DATABASE_URL")
}' >> ./prisma/schema.prisma

```

## Step 3. Pull Local DB Schema In schema.prisma

```
npx prisma db pull
```

## Step 4. Mark Migration v1.0.0 as completed, Because DB is already in sync

```
export DATABASE_URL="postgresql://postgres:mysecretpassword@localhost:5433/postgres?schema=prod"

npx prisma migrate resolve --applied v1.0.0
```

## Step 5. Make Changes In Local DB

```
ALTER TABLE pokemon RENAME COLUMN combat_power TO combat_power_level;
```

## Step 7. Pull New Local DB Schema Changes In schema.prisma

```
export DATABASE_URL="postgresql://postgres:mysecretpassword@localhost:5435/postgres?schema=local"

npx prisma db pull

export SHADOW_DATABASE_URL="postgresql://postgres:mysecretpassword@localhost:5434/"

npx prisma migrate diff --from-migrations ./prisma/migrations --to-schema-datamodel "./prisma/schema.prisma" --shadow-database-url "$SHADOW_DATABASE_URL" --script > migration.sql

mkdir -p prisma/migrations/v2.0.0

mv migration.sql prisma/migrations/v2.0.0
```

## Step 8. Verify the generated migration file

As our migration file is not as per out expectation, we have changed this to the below SQL command 👇
```
ALTER TABLE "pokemon" RENAME COLUMN "power" TO "power_level";
```

## Step 9. Run Migration On Prod DB

```
export DATABASE_URL="postgresql://postgres:mysecretpassword@localhost:5433/postgres?schema=prod"

npx prisma migrate deploy
```