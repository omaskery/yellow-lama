#include <boost/asio.hpp>
#include <stdexcept>
#include <signal.h>
#include <fstream>

#include "spacesim/networking/sim_server.hpp"
#include "spacesim/sim/simulation.hpp"
#include "spacesim/sim/physics_module.hpp"
#include "utils/json.hpp"

bool kill_flag = false;

void signal_handler(int _signal)
{
	kill_flag = true;
}

int main()
{
	const std::string savepath = "data/sim.state";
	
	struct sigaction signalHandler;
	signalHandler.sa_handler = signal_handler;
	sigemptyset(&signalHandler.sa_mask);
	signalHandler.sa_flags = 0;
	
	sigaction(SIGINT, &signalHandler, nullptr);
	
	std::cout << "starting server" << std::endl;
	
	try
	{
		boost::asio::io_service io_service;
		spacesim::sim::Simulation simulation;
		spacesim::networking::SimServer server(io_service, simulation, 40000);
		
		std::unique_ptr<spacesim::sim::PhysicsModule> physics(new spacesim::sim::PhysicsModule());
		
		simulation.add(std::move(physics));

		if(false)
		{
			simulation.load(savepath);
		}
		else
		{
			utils::json::Object planets;
			std::ifstream planetFile("data/planets.json");
			planetFile >> planets;
			
			for(const auto &planet : planets.fields())
			{
				spacesim::sim::PhysicalBody::UniquePtr entity(new spacesim::sim::PhysicalBody(planet));
				
				entity->setPosition(spacesim::sim::VectorFromJson(planets[planet]["pos"]));
				entity->setVelocity(spacesim::sim::VectorFromJson(planets[planet]["vel"]));
				entity->setRadius(planets[planet]["radius"].asDouble());
				entity->setMass(planets[planet]["mass"].asDouble());
				
				if(entity->name() == "Sun")
				{
					entity->setFixed(true);
				}
				
				simulation.add(std::move(entity));
			}
		}

		while(!kill_flag)
		{
			io_service.poll();
			simulation.update();
		}

		simulation.save(savepath);
	}
	catch (std::exception& e)
	{
		std::cerr << e.what() << std::endl;
	}
	
	std::cout << "\rstopping server" << std::endl;
	
	return 0;
}
