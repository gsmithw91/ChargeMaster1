package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"

	_ "github.com/denisenkom/go-mssqldb"
)

var db *sql.DB

func main() {
	initDB()
	defer db.Close()

	// Your server setup and other handlers...
}

func initDB() {
	var err error
	connString := getConnectionString()
	db, err = sql.Open("sqlserver", connString)
	if err != nil {
		log.Fatal("Open connection failed: ", err.Error())
	}

	err = db.Ping()
	if err != nil {
		log.Fatal("Cannot connect: ", err.Error())
	}
}

func getConnectionString() string {
	appEnv := os.Getenv("APP_ENV")
	if appEnv == "server" {
		// Connection string for the server
		return fmt.Sprintf("sqlserver://SA:B90b909021!@172.234.28.216:1433?database=ChargeMaster_Users&TrustServerCertificate=yes")
	} else {
		// Connection string for the desktop
		return fmt.Sprintf("sqlserver://username:password@DESKTOP-MPVS60R\\MSSQLSERVER01:1433?database=ChargeMaster_Users&TrustServerCertificate=yes&Integrated Security=SSPI")
	}
}
