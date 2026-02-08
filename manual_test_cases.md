# Casos de Prueba Manuales

Formato solicitado: ID del caso, Objetivo, Precondiciones, Pasos, Resultado Esperado, Resultado Obtenido, Evidencia.

## TC-REG-001 — Registro de usuario
- **Objetivo:** Verificar que un usuario pueda registrarse correctamente.
- **Precondiciones:** App abierta en `http://localhost:5173/`.
- **Pasos Detallados:**
  1. Clic en botón `🔐 Iniciar sesión`.
  2. En el dropdown, ingresar correo y contraseña en sección “Crear cuenta”.
  3. Clic en `Registrarse`.
- **Resultado Esperado:** Aparece mensaje “¡Registro exitoso! Ahora puedes iniciar sesión.”
- **Resultado Obtenido:** ________
- **Evidencia:** Captura del formulario y del mensaje de éxito.

## TC-LOG-002 — Login válido
- **Objetivo:** Validar inicio de sesión con credenciales válidas.
- **Precondiciones:** Usuario registrado en Firebase.
- **Pasos Detallados:**
  1. Clic en `🔐 Iniciar sesión`.
  2. Ingresar correo y contraseña válidos en “Login”.
  3. Clic en `Iniciar sesión`.
- **Resultado Esperado:** El usuario aparece logueado y se muestra el dropdown con el email.
- **Resultado Obtenido:** ________
- **Evidencia:** Captura del estado autenticado (nombre de usuario en navbar).

## TC-ACC-003 — Acceso a contenido restringido
- **Objetivo:** Verificar que solo usuarios logueados vean “Mi Stack Tecnológico”.
- **Precondiciones:** Usuario logueado.
- **Pasos Detallados:**
  1. Iniciar sesión.
  2. Hacer scroll hasta sección “Mi Stack Tecnológico”.
- **Resultado Esperado:** La sección aparece visible con carrusel y grid de tecnologías.
- **Resultado Obtenido:** ________
- **Evidencia:** Captura de la sección visible.

## TC-CIN-004 — Modal de película (Cinema Explorer)
- **Objetivo:** Validar que se abra y cierre el modal “Info”.
- **Precondiciones:** App cargada y películas visibles.
- **Pasos Detallados:**
  1. Scroll a “Cinema Explorer”.
  2. Pasar el mouse sobre una tarjeta.
  3. Clic en botón `▶ Info`.
  4. Clic en `Cerrar`.
- **Resultado Esperado:** Modal se abre con información y se cierra correctamente.
- **Resultado Obtenido:** ________
- **Evidencia:** Capturas de modal abierto y cerrado.

## TC-TAB-005 — Sistema de Tabs
- **Objetivo:** Validar apertura y cierre de pestañas de color.
- **Precondiciones:** App cargada.
- **Pasos Detallados:**
  1. En “Color Tab Section”, clic en una pestaña.
  2. Verificar que la pestaña aparece arriba.
  3. Clic en “×” para cerrarla.
- **Resultado Esperado:** La pestaña se abre y se cierra sin errores.
- **Resultado Obtenido:** ________
- **Evidencia:** Captura de pestaña abierta y luego cerrada.

## TC-REG-006 — Regresión
- **Objetivo:** Verificar que el dropdown de login sigue funcionando después de cambios UI.
- **Precondiciones:** App cargada.
- **Pasos Detallados:**
  1. Clic en `🔐 Iniciar sesión`.
  2. Verificar que el formulario aparece.
  3. Clic en `Cerrar`.
- **Resultado Esperado:** El dropdown abre y cierra sin errores.
- **Resultado Obtenido:** ________
- **Evidencia:** Capturas de apertura y cierre.
