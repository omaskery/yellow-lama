#pragma once
#ifndef _INCLUDE_THINK_INTERFACE_HEADER_
#define _INCLUDE_THINK_INTERFACE_HEADER_

namespace spacesim
{
    namespace sim
    {
        class IThink
        {
        public:
            virtual void think(double _dt) = 0;
        };
    }
}

#endif
