Este repositorio es la plantilla del curso gratuito "Python básico para ingeniería de datos". La usan principiantes de LATAM que quizá nunca han programado. Escribe todos tus comentarios en español.

Revisa solo defectos introducidos por este PR. Prioriza, en este orden:

1. **Pruebas que califican mal.** Una prueba que se puede pasar con una solución incorrecta o incompleta, o que rechaza una solución correcta escrita de otra forma. Las pruebas son la calificación del alumno.
2. **Conceptos usados antes de enseñarse.** Si una guía, ejemplo o ejercicio usa algo que ninguna lección anterior explicó, es un defecto.
3. **Errores técnicos** en código, guías o mensajes de las pruebas.
4. **Portabilidad.** Debe funcionar igual en Windows (PowerShell nativo, sin WSL), macOS y Linux, con Python 3.10 y 3.13: rutas con `pathlib`, `encoding="utf-8"` explícito, `newline=""` con `csv`, comandos de terminal para PowerShell y bash.
5. **Mensajes de prueba.** Deben decir qué se esperaba, qué se obtuvo y dar una pista sin regalar la solución.
6. **Consistencia.** Conteos de pruebas y tiempos en README de la lección y `docs/plan-de-estudios.md`, nombres de funciones entre guía, ejercicio y prueba.
7. **Español.** Ortografía, acentos y términos consistentes. Identificadores sin acentos ni ñ.

Este repositorio no contiene soluciones: los `ejercicios.py` lanzan `NotImplementedError` a propósito. No lo reportes.

No comentes estilo que ya revisa ruff, ni propongas refactors sin un defecto observable. Cada hallazgo lleva severidad, evidencia, impacto y una corrección concreta. Si no hay hallazgos materiales, dilo claramente.
