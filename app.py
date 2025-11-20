from flask import Flask, request
import os
import logging
import sys

app = Flask(__name__)

# Configure logging to output to STDERR following Smukfest standards
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)

logger = logging.getLogger(__name__)

# Add WARN level (Smukfest uses WARN, not WARNING)
logging.addLevelName(logging.WARNING, 'WARN')

@app.route('/')
def index():
    return """
        <h1>Smukfest Log Tester</h1>
        <p>Test forskellige logniveauer og se output i STDERR</p>
        
        <style>
            .log-container {
                margin: 15px 0;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            .dropdown {
                display: none;
                position: absolute;
                background: #eee;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                z-index: 1000;
                margin-top: 5px;
            }
            button {
                margin: 2px;
                padding: 8px 16px;
                cursor: pointer;
            }
            .debug-btn { background-color: #e3f2fd; }
            .info-btn { background-color: #e8f5e9; }
            .warn-btn { background-color: #fff3e0; }
            .error-btn { background-color: #ffebee; }
        </style>

        <div class="log-container">
            <strong>DEBUG:</strong> Detaljeret teknisk information. Bruges kun ved fejlfinding.
            <br>
            <button class="debug-btn" onclick="toggleDropdown('dropdown-debug')">
                Test DEBUG log
            </button>
            <div id="dropdown-debug" class="dropdown">
                <a href="/test-debug?value=true"><button>Success scenario</button></a><br>
                <a href="/test-debug?value=false"><button>Fejl scenario</button></a>
            </div>
        </div>

        <div class="log-container">
            <strong>INFO:</strong> Almindelige beskeder om hvad systemet gør.
            <br>
            <button class="info-btn" onclick="toggleDropdown('dropdown-info')">
                Test INFO log
            </button>
            <div id="dropdown-info" class="dropdown">
                <a href="/test-info?value=true"><button>Success scenario</button></a><br>
                <a href="/test-info?value=false"><button>Fejl scenario</button></a>
            </div>
        </div>

        <div class="log-container">
            <strong>WARN:</strong> Noget gik ikke som forventet, men systemet fortsætter.
            <br>
            <button class="warn-btn" onclick="toggleDropdown('dropdown-warn')">
                Test WARN log
            </button>
            <div id="dropdown-warn" class="dropdown">
                <a href="/test-warn?value=true"><button>Success scenario</button></a><br>
                <a href="/test-warn?value=false"><button>Fejl scenario</button></a>
            </div>
        </div>

        <div class="log-container">
            <strong>ERROR:</strong> En fejl forhindrede noget i at blive udført. Kræver opmærksomhed.
            <br>
            <button class="error-btn" onclick="toggleDropdown('dropdown-error')">
                Test ERROR log
            </button>
            <div id="dropdown-error" class="dropdown">
                <a href="/test-error?value=true"><button>Success scenario</button></a><br>
                <a href="/test-error?value=false"><button>Fejl scenario</button></a>
            </div>
        </div>

        <script>
            function toggleDropdown(id) {
                // Hide all dropdowns
                var dropdowns = document.getElementsByClassName('dropdown');
                for (var i = 0; i < dropdowns.length; i++) {
                    if (dropdowns[i].id !== id) {
                        dropdowns[i].style.display = 'none';
                    }
                }
                
                // Toggle the selected dropdown
                var dropdown = document.getElementById(id);
                dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
            }

            // Hide dropdown if clicked outside
            window.onclick = function(event) {
                if (!event.target.matches('button')) {
                    var dropdowns = document.getElementsByClassName('dropdown');
                    for (var i = 0; i < dropdowns.length; i++) {
                        dropdowns[i].style.display = 'none';
                    }
                }
            }
        </script>
    """

@app.route('/test-debug')
def test_debug():
    """
    DEBUG: Detaljeret teknisk information. Bruges kun ved fejlfinding.
    """
    value = request.args.get('value', 'true')
    
    if value == 'true':
        logger.debug("Sender SQL-request: SELECT * FROM tickets WHERE user_id=12345 AND status='active'")
        logger.debug("API-kald til smukcrew-service: payload={'action': 'fetch_tickets', 'limit': 100}")
        return "DEBUG log testet (success scenario) - Check STDERR for logs"
    else:
        logger.debug("Database connection pool status: 8/10 connections in use")
        logger.debug("Cache miss for key 'user_session_abc123' - fetching from database")
        return "DEBUG log testet (fejl scenario) - Check STDERR for logs"

@app.route('/test-info')
def test_info():
    """
    INFO: Almindelige beskeder om hvad systemet gør.
    """
    value = request.args.get('value', 'true')
    
    if value == 'true':
        logger.info("Bruger abc123 loggede ind via appen.")
        logger.info("Startede importjob 'daily_sync' for billetdata.")
        return "INFO log testet (success scenario) - Check STDERR for logs"
    else:
        logger.info("Bruger def456 loggede ud efter 45 minutters session.")
        logger.info("Planlagt backup af ticket-database gennemført succesfuldt.")
        return "INFO log testet (fejl scenario) - Check STDERR for logs"

@app.route('/test-warn')
def test_warn():
    """
    WARN: Noget gik ikke som forventet, men systemet fortsætter.
    """
    value = request.args.get('value', 'true')
    
    if value == 'true':
        logger.warning("Timeout fra payment-service – forsøger igen om 5 sek.")
        logger.warning("Manglende felt 'email' i brugerprofil for bruger xyz789 – bruger standardværdi.")
        return "WARN log testet (success scenario) - Check STDERR for logs"
    else:
        logger.warning("API 'weather-service' svarede ikke inden for 10 sekunder - bruger cached data.")
        logger.warning("Ugyldig QR-kode scannet - billetten kunne ikke valideres, men systemet fortsætter.")
        return "WARN log testet (fejl scenario) - Check STDERR for logs"

@app.route('/test-error')
def test_error():
    """
    ERROR: En fejl forhindrede noget i at blive udført. Kræver opmærksomhed.
    """
    value = request.args.get('value', 'true')
    
    if value == 'true':
        logger.error("Kunne ikke gemme ticket i databasen. Operation afbrudt. Database returnerede fejlkode 1062 (duplicate entry).")
        logger.error("API 'payment-gateway' returnerede 500 – transaktion annulleret for ordre #45678.")
        return "ERROR log testet (success scenario) - Check STDERR for logs"
    else:
        logger.error("Kritisk fejl: Database connection lost. Alle aktive transaktioner rullet tilbage. Kontakt infrastruktur-teamet.")
        logger.error("Fejl: API 'ticket-service' svarede ikke. Billetter kunne ikke hentes. Prøv igen, eller kontakt backend-teamet.")
        return "ERROR log testet (fejl scenario) - Check STDERR for logs"

if __name__ == '__main__':
    port = os.environ.get('FLASK_PORT') or 8080
    port = int(port)
    
    # Log application startup
    logger.info("Smukfest Log Tester applikation startet på port {}".format(port))
    
    app.run(port=port, host='0.0.0.0', debug=False)
