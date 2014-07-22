#include <boost/asio.hpp>
#include <stdexcept>
#include <fstream>

#include "spacesim/networking/sim_server.hpp"
#include "spacesim/sim/simulation.hpp"
#include "utils/json.hpp"

int main()
{
	std::string savepath = "data/sim.state";
	
	try
	{
		boost::asio::io_service io_service;
		spacesim::sim::Simulation simulation;
		spacesim::networking::SimServer server(io_service, simulation, 40000);

		simulation.load(savepath);

		while(true)
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

  return 0;
}
