Directory for adding juvenile data of pups, this kind of structure is suggested :

```{csv}
Project;Cohort;CageID;IDblind;Condition;PupID;Sexe;flip.lat.p13;flip.AUC.p7.10;av.cliff.lat;av.geotax.lat;av.grasp.lat;norm.av.grasp.lat;av.front.lat;norm.av.front.lat;d.ear.twicth;d.ear.c.open;d.eye.l.open;d.transition;d.walk;exit.tube;BW.P3;BW.P4;BW.P5;BW.P6;BW.P7;BW.P8;BW.P9;BW.P10;BW.P11;BW.P12;BW.P13;BW.P16;tot.n.voc.p3;av.freq.p3;av.ep.dur.p3;lat.p3;tot.n.voc.p14;av.freq.p14;av.ep.dur.p14;lat.p14;Cortp;CDK9;DGKH;FKBP5;HSP90AA1;HSP90AB1;NFATC1;NR3C1;PTGES3;SGK1;SGK3;SKA2;STAT5A
```

Another type of file is needed here, for all the analysis : metadata file for linking maternal cages and pups ids (Sorry for the mess on columns names, follow this names even if it's ridiculous)

```{csv}
Project;Cohort;Group;Cage ID;ID blind;PupID;Sexe
VEAVE;Cohort 0;LBN;G;1t2;G5;Female
VEAVE;Cohort 0;LBN;G;354;G1;Male
VEAVE;Cohort 0;LBN;G;3t0;G3;Female
VEAVE;Cohort 0;LBN;G;r01;G4;Male
VEAVE;Cohort 0;LBN;G;t44;G2;Female
VEAVE;Cohort 0;LBN;G;st3;G6;Male
VEAVE;Cohort 1;LBN;A;1;A1;Female
VEAVE;Cohort 1;LBN;A;2;A2;Male
VEAVE;Cohort 1;LBN;A;3;A3;Male
VEAVE;Cohort 1;LBN;A;4;A4;Male
VEAVE;Cohort 1;LBN;A;5;A5;Male
VEAVE;Cohort 1;LBN;A;6;A6;Male
VEAVE;Cohort 1;LBN;A;7;A7;Male
VEAVE;Cohort 1;LBN;C ;1di;C1;Female
VEAVE;Cohort 1;LBN;C ;35d;C2;Female
VEAVE;Cohort 1;LBN;C ;2k0;C3;Female
VEAVE;Cohort 1;LBN;C ;fe3;C4;Female
VEAVE;Cohort 1;LBN;C ;9hc;C5;Female
VEAVE;Cohort 2;LBN;1;1;63;female
VEAVE;Cohort 2;LBN;1;2;64;female
VEAVE;Cohort 2;LBN;1;3;65;male
VEAVE;Cohort 3;LBN;2;4OR;C2-1;Male
VEAVE;Cohort 3;LBN;2;Q9E;C2-2;Male
VEAVE;Cohort 3;LBN;2;JFP;C2-3;Male
VEAVE;Cohort 3;LBN;2;DCL;C2-4;Male
VEAVE;Cohort 3;LBN;2;OP2;C2-5;Female
VEAVE;Cohort 3;LBN;2;EZO;C2-6;Male
VEAVE;Cohort 3;LBN;2;JCA;C2-7;Female
VEAVE;Cohort 3;LBN;3;J1A;C3-1;Female
VEAVE;Cohort 3;LBN;3;N2G;C3-2;Male
VEAVE;Cohort 3;LBN;3;DT7;C3-3;Male
VEAVE;Cohort 3;LBN;3;4T9;C3-4;Male
VEAVE;Cohort 3;LBN;3;3DC;C3-5;Female
VEAVE;Cohort 3;LBN;3;89H;C3-6;Male
VEAVE;Cohort 3;LBN;3;J9K;C3-7;Male
VEAVE;Cohort 3;LBN;7;ilyapas;C7-1;Female
VEAVE;Cohort 3;LBN;7;BUV;C7-2;Female
VEAVE;Cohort 3;LBN;7;NCX;C7-3;Male
VEAVE;Cohort 3;LBN;7;UAO;C7-4;Male
VEAVE;Cohort 3;LBN;7;IG9;C7-5;Female
VEAVE;Cohort 3;LBN;7;O1I;C7-6;Male
VEAVE;Cohort 3;LBN;7;ZZT;C7-7;Male
VEAVE;Cohort 3;LBN;9;8EY;C9-1;Male
VEAVE;Cohort 3;LBN;9;5PL;C9-2;Male
VEAVE;Cohort 3;LBN;9;9LD;C9-3;Female
VEAVE;Cohort 3;LBN;9;YNP;C9-4;Male
VEAVE;Cohort 3;LBN;9;YWC;C9-5;Female
VEAVE;Cohort 3;LBN;9;W3Y;C9-6;Female
VEAVE;Cohort 3;CONT;C1;EG9;C1-1;Male
VEAVE;Cohort 3;CONT;C1;1C3;C1-2;Male
VEAVE;Cohort 3;CONT;C1;ilyapas2;C1-3;Male
VEAVE;Cohort 3;CONT;C1;NW6;C1-4;Female
VEAVE;Cohort 3;CONT;C1;UKN;C1-5;Female
VEAVE;Cohort 3;CONT;C1;L36;C1-6;Female
VEAVE;Cohort 3;CONT;C1;ilyapas3;C1-7;Female
VEAVE;Cohort 3;CONT;6;6P4;C6-1;Female
VEAVE;Cohort 3;CONT;6;LK9;C6-2;Male
VEAVE;Cohort 3;CONT;6;MNT;C6-3;Female
VEAVE;Cohort 3;CONT;6;9FY;C6-4;Male
VEAVE;Cohort 3;CONT;6;R6H;C6-5;Female
VEAVE;Cohort 3;CONT;6;T5M;C6-6;Female
VEAVE;Cohort 3;CONT;8;UKO;C8-1;Female
VEAVE;Cohort 3;CONT;8;S5L;C8-2;Female
VEAVE;Cohort 3;CONT;8;C3Y;C8-3;Female
VEAVE;Cohort 3;CONT;8;D35;C8-4;Male
VEAVE;Cohort 3;CONT;8;YL5;C8-5;Male
VEAVE;Cohort 3;CONT;8;HJT;C8-6;Male
VEAVE;Cohort 3;CONT;8;RG2;C8-7;Female
VEAVE;Cohort 2;CONT;K1;1;66;male
VEAVE;Cohort 2;CONT;K1;2;67;male
VEAVE;Cohort 2;CONT;K1;3;68;female
VEAVE;Cohort 2;CONT;K1;4;69;male
VEAVE;Cohort 0;CONT;E;320;E3;Female
VEAVE;Cohort 0;CONT;E;51t;E1;Male
VEAVE;Cohort 0;CONT;E;t50;E2;Female
VEAVE;Cohort 1;CONT;D;hc6;D2;Female
VEAVE;Cohort 1;CONT;D;7l4;D3;Male
VEAVE;Cohort 1;CONT;D;1ag;D4;Female
VEAVE;Cohort 1;CONT;D;fc1;D5;Female
VEAVE;Cohort 1;CONT;D;e1b;D1;Male
```
