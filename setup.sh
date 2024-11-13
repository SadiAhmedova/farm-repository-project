
if [ -f .env ]; then
	  echo ".env file already exists. Please edit it manually."
  else
	      cp .env.example .env

		  echo ".env file created. Please edit it with your configuration values."
fi

