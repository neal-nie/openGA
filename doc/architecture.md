# Arichecture of openGA

<p align="right">by Nie Guangze</p>

## Class

- Chromosome

    ```puml
    @startuml
    Class Chromosome {
        float[] genes
        str[] names
        (Chromosome, Chromosome) crossover(Chromosome couple, float eta)
        Chromosome mutate(float eta)
    }
    @enduml
    ```

- Individual

    ```puml
    @startuml
    Class Individual {
        int gen_id
        int idv_id
        float fittness
        Chromosome plasm
        --patch--
        express()
        evaluate()
    }
    @enduml
    ```

- Population

    ```puml
    @startuml
    Class Population {
        int gen_id
        int size
        Individual[] curr_gen
        Individual[] children
        Individual[] next_gen
        --public--
        Individual[] compete(int pool_size, int tour_size)
        Individual[] reproduce()
        Individual[] elmiate()
        --private--
        individual[] combine()
        individual[] select()
        evaluate()
    }
    @enduml
    ```

## Framework

`ToDo`
