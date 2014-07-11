#include <boost/asio.hpp>
#include <stdexcept>

#include "spacesim/networking/sim_server.hpp"

int main()
{
  try
  {
    boost::asio::io_service io_service;
    spacesim::networking::SimServer server(io_service, 40000);
    
    while(true)
    {
		io_service.poll();
	}
  }
  catch (std::exception& e)
  {
    std::cerr << e.what() << std::endl;
  }

  return 0;
}
