import asyncio

from get_links import link_parse

async def rug_check():
	data = await link_parse()
	
	if data is None:
		return
		
	name = data[0]
	mint = data[1]
	link_type = data[2]
	username = [3]
 
	if link_type == 'user':
		pass
	elif link_type == 'community':
		pass

if __name__ == '__main__':
	asyncio.run(rug_check())