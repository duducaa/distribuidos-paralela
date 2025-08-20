# Round Robin Simulation

Este projeto simula um **escalonador Round Robin** de processos.

- Existem 4 processos criados aleatoriamente.  
- Cada processo recebe um "programa" (zscore, minmax ou clip).  
- O quantum é escolhido aleatoriamente (1, 2 ou 3).  
- O processo pode ser bloqueado, executado ou terminado.  
- O log mostra a evolução do estado de cada processo no tempo.  

## Como rodar
```bash
pip install numpy
python scheduler.py
