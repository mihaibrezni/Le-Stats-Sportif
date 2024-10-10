1. Cum rulezi:
- initializare mediu virtual:
    -  python -m venv venv
    -  source venv/bin/activat
    -  python -m pip install -r requirements.txt
    -  make create_venv
    -  source venv/bin/activate
    -  make install
- pornire server
    - source venv/bin/activate
    - make run_server
- pornire teste 
    - source venv/bin/activate
    - make run_tests
    - 
1. Explicație pentru soluția aleasă:

- Pentru a rezolva probleama cu multithreading am ales să folosesc un ThreadPoolExecutor. Folosim un pool pentru a executa mai multe taskuri în paralel. Acesta este util atunci când avem de executat mai multe taskuri care nu depind unul de celălalt, precum functiile noastre, fara sa astepte una dupa alta, fapt ce ar fi putut duce la un posibil deadlock.
- Fiecare functie este transmisa prin submit la executor de unde este pornita comcomitent cu restul functiilor.
- Prin functia stop, serverul nu mai primeste taskuri, dar asteapta ca sa se finalizeze taskurile curente.
- Fiecare functie am ales sa fie creata in clasa unde se afla executorul pentrua  grupa codul. Fiecare functie primeste paramatri si este apelata de catre server un functie de ce API primeste si ce metoda avem.
- Ficare functie are o descriere a ceea ce face si ce parametri primeste, returneaza un status si ofera un raspuns sub forma de fisier.
- /api/jobs si /api/num_jobs au fost mai mult testate manual si ofera info cu referire la taskurile curente si la numarul de taskuri.

- curl -X POST -H "Content-Type: application/json" -d '{"question": "Percent of adults aged 18 years and older who have an overweight classification"}' http://127.0.0.1:5000/api/states_mean