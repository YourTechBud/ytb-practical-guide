-- CreateTable
CREATE TABLE "pokemon" (
    "id" SERIAL NOT NULL,
    "name" VARCHAR(100),
    "power" INTEGER,
    "caught_on" TIMESTAMP(6),
    "trainer_id" INTEGER,

    CONSTRAINT "pokemon_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "trainer" (
    "id" SERIAL NOT NULL,
    "name" VARCHAR(100),
    "city" VARCHAR(100),

    CONSTRAINT "trainer_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "pokemon" ADD CONSTRAINT "pokemon_trainer_id_fkey" FOREIGN KEY ("trainer_id") REFERENCES "trainer"("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

