(define (domain monkeyproblem)
   (:requirements :strips)
   (:constants monkey box bananas)
   (:predicates 
                 (location ?x)
                 (at ?x ?x)
                 (on-floor)
                 (hasbananas)
                 (onbox ?x)
                 )
                 
    (:action goto
             :parameters (?x ?y)
             :precondition (and 
                            (location ?x)
                            (location ?y)
                             (on-floor)
                             (at monkey ?y)
                             )
             :effect  (and 
                           (at monkey ?x)
                           (not (at monkey ?y))
                           )
    ) 
    
       (:action climb
            :parameters (?x)
            :precondition (and
                                (location ?x)
                                (at monkey ?x)
                                (at box ?x)
                                )
            :effect  (and 
                        (onbox ?x)
                        (not (on-floor))
                        )   
     ) 
    
    (:action push-box
             :parameters (?x ?y)
             :precondition (and
                                (location ?x)
                                (location ?y)
                                (on-floor)
                                (at monkey ?y)
                                (at box ?y)
                                )
    
             :effect  (and 
                           (at monkey ?x)
                           (at box ?x)
                           (not (at monkey ?y))
                           (not (at box ?y))
                           )
    ) 
    
     (:action grab-bananas
             :parameters (?y)
             :precondition (and 
                             (location ?y)
                             (at monkey ?y)
                             (at bananas ?y)
                             (onbox ?y)
                             )
             :effect  (and 
                           (hasbananas)
                           )
    ) 
) 